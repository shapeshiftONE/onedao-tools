import os
import re
import requests
import string
import datetime
from dataclasses import dataclass, field
from bs4.element import Tag
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from slugify import slugify
from input import library_newsroom

WORD_RATE=0.05 # Rate in USD per word.
MAX_DESCRIPTION_LEN=140 # Maximum length of the description.
BOUNTY_ADDRESS='0xFAc9dD5194098461B627554347f83D5431Fb30e2'

import_urls = library_newsroom.import_urls

markdown_template = """---
title: {doc.title}
description: {doc.description}
published: {doc.published}
date: {doc.currentISODatetime}
tags: {doc.joinedTags}
editor: {doc.editor}
dateCreated: {doc.currentISODatetime}
---

# {doc.title}

{doc.markDownContent}

---

> This document was originally published on {doc.originalDate} by {doc.author} and may have been slightly modified for translation by the Information and Globalization workstream for an ongoing archival project.
>
> Original article can be found [here]({doc.originalURL}).
{{.is-success}}

---

- bounty: true
- amt: {bountyAmt}
- signedBy: {bountyAddress}
- hash: 
{{.is-hidden}}\
"""

# Document data structure
@dataclass
class Document:
    title: str = None
    description: str = None
    originalDatetime: datetime.datetime = None
    currentDatetime: datetime.datetime = None
    author: str = None
    tags: list = field(default_factory=list)
    published: bool = True
    editor: str = 'markdown'
    htmlContent: Tag = None
    markDownContent: str = None
    originalURL: str = None
    slug: str = None
    
    @property
    def joinedTags(self) -> str:
        return ', '.join(self.tags)

    @property
    def originalDate(self) -> str:
        return self.originalDatetime.strftime('%Y-%m-%d')

    @property
    def originalDateShort(self) -> str:
        return self.originalDatetime.strftime('%B %Y')

    @property
    def currentISODatetime(self) -> str:
        # Force UTC by adding "Z", easier than setting the TZ in the datetime object.
        return currentDoc.currentDatetime.isoformat(timespec='milliseconds') + 'Z'

    @property
    def wordCount(self) -> int:
        # Tag words + Title + Content
        text = " ".join(self.tags) + self.title + " " + self.description + " " + self.htmlContent.get_text()
        text_noPunc = text.translate(str.maketrans("","", string.punctuation))
        words = text_noPunc.split()
        return len(words) + len(self.tags)

# Utils
def smart_truncate(content, length=100, suffix=' ...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

# Fixes for Markdown, specific to Shapeshift.com Content
def fixBr(text):
    # Remove lone <br/>'s that are in bold and then italic, they are invisible anyways.
    for search in ['**<br/>**', '*<br/>*']:
        if search in text:
            text = text.replace(search,' ')
    # Remove end of bold/italic <br/>'s that break the styling.
    text = re.sub(r'^(\*.+)<br/>\s*(\*)$', r'\1\2', text, flags=re.MULTILINE)
    text = re.sub(r'^(\*\*.+)<br/>\s*(\*\*)$', r'\1\2', text, flags=re.MULTILINE)
    # Add newline when <br/> was used inside a numbered list.
    text = re.sub(r'(<br/>)(\*?)([0-9]+\. )', r'\1\2\n\3', text)
    return text

def fixWhiteSpace(text):
    # Remove empty unicode whitespace characters.
    for ch in ['\u00a0', '\u200d']:
        if ch in text:
            text = text.replace(ch,' ')
    return text
    
def fixMDHeadings(text):
    # Move headings which are not at the start of by adding two newlines before them
    text = re.sub(r'^([^#]+)(##+)', r'\1\n\n\2', text, flags=re.MULTILINE)
    # All Headings above h1 become h2, none of the documents seem to need h3 and above
    # visually (if they do they'll get fixed manually)
    text = re.sub(r'^#[#]{2,5}', r'##', text, flags=re.MULTILINE)
    # Some headings start with a <br/> which makes no sense, removes them <br/>
    # if spacing is needed it should be done with CSS
    text = re.sub(r'^(##?)\s*<br/>\s*', r'\1 ', text, flags=re.MULTILINE)
    return text

def fixEmptyInlinesEOL(text):
    # Remove empty useless bold/italics at the end of lines
    text = re.sub(r'\*\*\s+\*\*$', r'', text, flags=re.MULTILINE)
    text = re.sub(r'\*\s+\*$', r'', text, flags=re.MULTILINE)
    return text

def fixSuperfluousNewlines(text):
    # Reduces successive empty new lines to 1 (including when a line has only whitespace)
    return re.sub(r'\n\s*\n', r'\n\n', text)

# Chain Markdown fixes, order matters.
def fixMarkDown(text):
    return fixSuperfluousNewlines(fixEmptyInlinesEOL(fixMDHeadings(fixBr(fixWhiteSpace(text)))))

# Custom MarkdownConverter to override certain features
class CustomerMarkDownConverter(MarkdownConverter):
    # Two newlines after images for spacing
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'

    # Do not replace <br/>'s
    def convert_br(self, el, text, convert_as_inline):
        return str(el)
    
    # Leave iframes as is (without their former container)
    def convert_iframe(self, el, text, convert_as_inline):
        return str(el) + "\n\n"

# Shorthand to use the custom markdownify class.
def md(html, **options):
    return CustomerMarkDownConverter(**options).convert(html)

totalBountyAmount = 0
# Each dictionary key will be used as a directory.
for category in import_urls:
    totalCatBountyAmount = 0
    for import_url in import_urls[category]:
        currentDoc = Document()
        r = requests.get(import_url)
        s = BeautifulSoup(r.content, 'html.parser')
        currentDoc.originalURL = import_url
        currentDoc.title = s.h1.text.replace(': ', ' - ')
        currentDoc.originalDatetime = datetime.datetime.strptime(s.find(attrs={'class': 'single-posted-on'}).text, '%B %d, %Y')
        currentDoc.currentDatetime = datetime.datetime.now()
        # List of tags, the string version is a property of this object.
        currentDoc.tags = list(map(lambda x: x.lower(), s.find(attrs={'class': 'single-tags-wrapper'}).strings))
        currentDoc.tags.append('needs-review')
        currentDoc.author = s.find(attrs={'class': 'single-posted-author'}).text
        # Prop an empty article if the article has no content
        currentDoc.htmlContent = s.find(attrs={'class': 'post-content w-richtext'}) or BeautifulSoup('', 'html.parser')
        currentDoc.markDownContent = fixMarkDown(md(str(currentDoc.htmlContent), heading_style='atx').strip())
        subtitle = s.find(attrs={'class': 'lockup-internal-subhead'}).text
        # Use the subtitle as description if it exists, or a excerpt of the article otherwise.
        currentDoc.description = smart_truncate((subtitle if len(subtitle) > 0 else currentDoc.htmlContent.text), MAX_DESCRIPTION_LEN)
        bountyAmount = int(round(currentDoc.wordCount*WORD_RATE,0))
        totalCatBountyAmount += bountyAmount
        outputContent = markdown_template.format(doc=currentDoc, bountyAmt=bountyAmount, bountyAddress=BOUNTY_ADDRESS)
        # Build filename from date and title
        currentDoc.slug = slugify(currentDoc.originalDateShort + " " + currentDoc.title)
        outputFilename = f'output/{category}/{currentDoc.slug}.md'
        os.makedirs(os.path.dirname(outputFilename), exist_ok=True)
        with open(outputFilename, 'w', encoding="utf-8") as f:
            f.write(outputContent)
            print(f'[{currentDoc.originalURL}] converted to MarkDown in [{outputFilename}]')
    totalBountyAmount += totalCatBountyAmount
    print(f'Total Bounty Amount for {category}: {totalCatBountyAmount}')
print(f'Grand Total Bounty Amount: {totalBountyAmount}')
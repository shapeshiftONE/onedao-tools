import os
import requests
import datetime
from bs4 import BeautifulSoup
from slugify import slugify
from input import library_newsroom, output_templates
from models import Document
from utils import fixMarkDown, smart_truncate
from custom_markdownify import custom_markdownify

WORD_RATE = 0.05 # Rate in USD per word.
MAX_DESCRIPTION_LEN = 140 # Maximum length of the description.
BOUNTY_ADDRESS = '0xFAc9dD5194098461B627554347f83D5431Fb30e2'

import_urls = library_newsroom.import_urls
markdown_template = output_templates.default_markdown

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
        currentDoc.markDownContent = fixMarkDown(custom_markdownify(str(currentDoc.htmlContent), heading_style='atx').strip())
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
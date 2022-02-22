import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Trucate a string if needed and ads a suffix.
def smart_truncate(content, length=100, suffix=' ...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

# Fixes for Markdown, specific to Shapeshift.com Content.
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

def singleLine(text, delimiter=' '):
    # Transform a multiple line string into a single line, replacing new lines by a delimiter (default is a space character)
    # text = fixSuperfluousNewlines(text).strip()
    return re.sub(r'\n\n*', r'{delimiter}', text).strip()

def expandRelativeURL(s: BeautifulSoup, base_url):
    # Replaces relative URL for anchors and images in a BeautifulSoup tree with absolute ones, based on the base URL.
    for link in s.find_all(name={'a'}, attrs={'href': True}):
        link.attrs['href'] = urljoin(base_url, link.attrs['href'])
    for img in s.find_all(name={'img'}, attrs={'src': True}):
        img.attrs['src'] = urljoin(base_url, img.attrs['src'])

# Chain Markdown fixes, order matters.
def fixMarkDown(text):
    return fixSuperfluousNewlines(fixEmptyInlinesEOL(fixMDHeadings(fixBr(fixWhiteSpace(text)))))
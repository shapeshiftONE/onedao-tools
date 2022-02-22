# Settings file import
from input import helpdesk as input_settings, output_templates
from input import output_templates
import os
import requests
from fake_useragent import UserAgent
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from slugify import slugify
from models import Document
from utils import expandRelativeURL, fixMarkDown, smart_truncate, singleLine
from custom_markdownify import custom_markdownify

WORD_RATE = 0.05 # Rate in USD per word.
MAX_DESCRIPTION_LEN = 140 # Maximum length of the description.
BOUNTY_ADDRESS = '0xFAc9dD5194098461B627554347f83D5431Fb30e2'

# Settings files for the data source.
import_urls = input_settings.import_urls
import_params = input_settings.import_params
# Output template.
markdown_template = output_templates.default_markdown

ua = UserAgent()
totalBountyAmount = 0
# Each dictionary key will be used as a directory.
for category in import_urls:
    totalCatBountyAmount = 0
    for import_url in import_urls[category]:
        currentDoc = Document()
        # Request using a common User Agent (many sites will filter requests without this).
        r = requests.get(import_url, headers={'User-Agent': ua.chrome}, allow_redirects=False)
        # Report errors for failed HTTP queries.
        if (r.status_code != 200):
            print(f'ERROR: [{import_url}] could not be directly reached [HTTP Code: {r.status_code}]')
            continue
        # Parse the successful reponse into a BeautifulSoup tree.
        s = BeautifulSoup(r.content, 'html.parser')
        # Fix relative URLs for anchors and images in the HTML soup.
        expandRelativeURL(s, import_url)
        currentDoc.originalURL = import_url
        currentDoc.title = s.find(**import_params['title']).text.replace(': ', ' - ').strip()
        # Extract and format document date.
        dateElement = s.find(**import_params['date'])
        dateValue = dateElement.get(import_params['date_attr']) if 'date_attr' in import_params and import_params['date_attr'] else dateElement.text
        currentDoc.originalDatetime = datetime.datetime.strptime(dateValue, import_params['date_format'])
        currentDoc.currentDatetime = datetime.datetime.now()
        # Insert the current category as first tag.
        currentDoc.tags = [category]
        # List of tags, the string version is a property of this object.
        if 'tags' in import_params and import_params['tags']:
            currentDoc.tags += list(map(lambda x: x.lower(), s.find(**import_params['tags']).strings))
        currentDoc.tags.append('needs-review')
        # Make tags unique and preserve order.
        currentDoc.tags = list(dict.fromkeys(currentDoc.tags))
        authorContent = s.find(**import_params['author']).contents
        currentDoc.author = authorContent[0].strip() if len(authorContent) > 0 else 'Unknown'
        # Prop an empty article if the article has no content.
        currentDoc.htmlContent = s.find(**import_params['content']) or BeautifulSoup('', 'html.parser')
        currentDoc.markDownContent = fixMarkDown(custom_markdownify(str(currentDoc.htmlContent), heading_style='atx').strip())
        # Get subtitle if defined/available.
        subtitle = s.find(**import_params['subtitle']).text if 'subtitle' in import_params and import_params['subtitle'] else ''
        # Use the subtitle as description if it exists, or a excerpt of the article otherwise.
        currentDoc.description = smart_truncate(singleLine((subtitle if len(subtitle) > 0 else currentDoc.htmlContent.text)), MAX_DESCRIPTION_LEN)
        bountyAmount = int(round(currentDoc.wordCount*WORD_RATE,0))
        totalCatBountyAmount += bountyAmount
        outputContent = markdown_template.format(doc=currentDoc, bountyAmt=bountyAmount, bountyAddress=BOUNTY_ADDRESS)
        # Build filename from date and title.
        currentDoc.slug = slugify(currentDoc.originalDateShort + " " + currentDoc.title)
        outputFilename = f'output/{category}/{currentDoc.slug}.md'
        os.makedirs(os.path.dirname(outputFilename), exist_ok=True)
        with open(outputFilename, 'w', encoding="utf-8") as f:
            f.write(outputContent)
            print(f'[{currentDoc.originalURL}] converted to MarkDown in [{outputFilename}]')
    totalBountyAmount += totalCatBountyAmount
    print(f'Total Bounty Amount for {category}: {totalCatBountyAmount}')
print(f'Grand Total Bounty Amount: {totalBountyAmount}')
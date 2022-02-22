# Mostly arguments to pass to BeautifulSoup.find() to search in the HTML soup
import_params = {
    'title': {'name': 'h1'},
    'date': {'name': 'time'},
    'date_attr': 'datetime',  # If the date is within an attribute of the element specify it here.
    'date_format': '%Y-%m-%dT%H:%M:%SZ', # Format of the date on the source
    'tags': None,
    'author': {'attrs': {'class': 'article-meta'}},
    'content': {'attrs': {'class': 'article-content'}},
    'subtitle': None,
}
# From: https://shapeshift.zendesk.com
import_urls = {
    'helpdesk-faq': [
        'https://shapeshift.zendesk.com/hc/en-us/articles/4415257259533-Airdrop-FAQ',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4411531987597-Rewards-Ending-October-31-2021',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4405155758989-ShapeShift-DAO-Terminology',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4405013879693-What-is-Happening-with-KeepKey-the-ShapeShift-Mobile-App-and-beta-shapeshift-com-',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4404959296397-Decentralized-ShapeShift-What-Does-it-Mean-',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4404959289229-FOX-Governance',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4404943013005-Important-Links-When-Interacting-with-the-ShapeShift-DAO',
        'https://shapeshift.zendesk.com/hc/en-us/articles/360014255940-For-Developers',
        'https://shapeshift.zendesk.com/hc/en-us/articles/360013581619-Request-a-Feature',
        'https://shapeshift.zendesk.com/hc/en-us/articles/360000591420-What-is-a-FOX-Token-',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4422161472909-ShapeShift-DAO-S-Current-CEX-DEX-Listings',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4424444368013-Does-ShapeShift-Have-A-Merch-Store-'
    ],
    'helpdesk-governance': [
        'https://shapeshift.zendesk.com/hc/en-us/articles/4406066341645-FOX-Governance-Process',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4405767883149-Voting-in-The-Boardroom',
        'https://shapeshift.zendesk.com/hc/en-us/articles/4405762667789-How-to-Formally-Vote-on-a-ShapeShift-DAO-Proposal',
    ]
}

# oneDAO Feed Generation

A lot of unorthodox RSS scraping and feed generation going on here, which I'll explain more in depth later. Short explanation: the client front-facing site will be static generated via Nuxt and Vue, which allows for hosting in a decentralized environment (IPFS, Arweave, Sia, etc) without having to make external API calls. 

This package is a small part of a much larger project, so some things may feel out of place. 

## Publications or Feed Providers

The list of publications is in testPubs.json, and is currently used for ... well, testing purposes. Publications will eventually be swapped out for DAO related feeds.

## Custom Feed Generation

Not all content, data, and feeds have an RSS feed to work off of. In these cases, a custom feed can be created that meets the specifications of this tool; more on this later.

## Full Text Scraping

Selenium and BS4 is used to go one level deeper to get the full text content. Simply change the CSS selector for the particiular publisher in testPubs.json for the `fullSelector` key. A bit of CSS knowledge and trickery may be required for some publishers. 

*Practice Responsible Scraping:* Not all publishers are too fond of crawlers crawlin' their content. Since our feeds will most likely be DAO-related content, it shouldn't be a problem; but use good ethics and judgement when using for external publishers. In most cases, they will have an API or graph we can call, which we can then use to create a simple RSS feed so that our structured flow of information is consistent. 

## Supabase and Storage

The client site uses Supabase as its FOSS self-hosted "Firebase" alternative for database and user management. I'll upload the db schematics after some more tinkering, but for now ask me for the auth keys. Most recent feed data are stored as a json file to take advantage of Nuxt's Content module for that super foxy speed and performance (experimenting). The content is stored and can be automatically rotated out with Github Actions (check `commit.sh`). At the moment its just there as a POC, no real point as the platform will first be hosted on a centralized server.

## Running the Script

`yarn` to first initialize the package and install dependencies. 

`yarn gen` will execute `node scripts/index.js && node scripts/getText.js`
`yarn gen meta` will scrape only the metadata.
`yarn gen full` will only run the full text scraper.

Since this package was haphazardly taken from a bigger project there's a good chance that you may run into dependency problems or some error. Let me know when you do and we'll take figure it out.
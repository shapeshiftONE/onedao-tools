# Templates for the output

default_markdown = """---
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
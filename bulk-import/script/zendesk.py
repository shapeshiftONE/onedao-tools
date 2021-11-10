import pandas as pd
from slugify import slugify
import re
regex = r"<img[^>]+src=\"/hc"
subst = "<img src=\"https://shapeshift.zendesk.com/hc"

def createMeta(title, desc, date, tags, content, ogLink, lastUpdated):
	meta = '''<!--
title: {0}
description: {1}
published: true
date: {2}
tags: {3}
editor: ckeditor
-->

<h1>{0}</h1>
{4}
<hr>
<div class="meta-footer">
<p>Documented archived by the ShapeShift DAO Information and Globalization workstream for translation purposes. Original article can be found <a href="{5}" target="_blank">here.</a></p>
<p>Last updated: {6}</p>
</div>
	'''
	return meta.format(title, desc, date, tags, content, ogLink, lastUpdated)

df = pd.read_csv("portis.csv")
tags = 'portis, portis wallet, wallet, zendesk, portis-zendesk'
date = '2021-11-01T12:38:32.281Z'
for index, row in df.iterrows():
	title = row[0]
	slug = slugify(title)
	ogLink = row[1]
	lastUpdated = row[2]
	content = row[3]
	result = re.sub(regex, subst, content, 0, re.IGNORECASE)

	desc = row[4]

	htmlfile = createMeta(title, desc, date, tags, result, ogLink, lastUpdated)

	print(htmlfile)
	fileName = 'portis/{}.html'.format(slug)
	print(fileName)
	try:
		f = open(fileName,'w')
		f.write(htmlfile)
		f.close()
	except:
		pass


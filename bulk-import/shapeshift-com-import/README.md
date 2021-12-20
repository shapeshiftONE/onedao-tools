# shapeshift-com-import

## Description

This tool imports HTML content from `shapeshift.com` blog articles and convert them to MarkDown format follwing a template supported by the `docs.shapeshift.one` plafrom

## Requirements

* Python 3.10
* Dependencies listed in `requirements.txt`


## Installation

```
$ pip install -r requirements.txt
```

## Usage

Configure the URL of the documents you want to import in `input/library_newsroom.py`. The script expects a dictionary of category keys, each holding a list of URL strings of articles to import.

You can also tweak the output template in `input/output_templates.py`

Then simply run:

```
$ python main.py
```

The process reports each file it imported and where it was placed. Imported files are placed in an `output` folder, relative to the script folder, each category gets its own sub-folder in it.
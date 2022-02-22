# shapeshift-com-import

## Description

This tool imports HTML content originally from `shapeshift.com` blog articles and convert them to MarkDown format following a template supported by the `docs.shapeshift.one` platform.

With additional parameters in the input template file this tool can be adapted for other data sources by identifying the proper HTML elements/attributes and other settings. See "Usage" for more details.

## Requirements

* Python 3.10
* Dependencies listed in `requirements.txt`


## Installation

```
$ pip install -r requirements.txt
```

## Settings

Configure the parameters and list of URL of the documents you want to import based on the sample template: `input/library_newsroom.py`.

It contains 2 required variables that must be imported in the main script:

### `import_params`

A dictionary of fields used in the output matched with the HTML elements that should be extracted from the source documents. More detail for each dictionary entry and how they are used in the comments.

### `import_urls`

A dictionary of category keys, each entry holding a list of URL for the documents to import. The category keys are added as a tag for each article within it to help sorting them on the platform.

Make sure you import the input file you have built (first line of the main script) and that it contains those two variables in the proper format.

You can also tweak the output template in `input/output_templates.py`
## Usage 
Then simply run:

```
$ python main.py
```

The process reports each file it imported and where it was placed. Imported files are placed in an `output` folder, relative to the script folder, each category gets its own sub-folder in it.
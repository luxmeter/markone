# MarkOne

Local web app rendering your markdown files automatically while you edit them in your favorite editor.

## Overview

MarkOne is a small web app that is supposed to be run locally
to render your markdown files automatically after you edited them
with your favorite editor, e.g. vim.

![MarkOne](https://raw.githubusercontent.com/luxmeter/markone/master/markone.gif)

## Installation

Install the app (preferred in a virtual environment):

    $ pip install markone

If you want to build it yourself, you first need to install pipenv
that feeds setup.py with the project dependencies:

    $ pip install pipenv

Afterwards you can install the app from source code:

    $ git clone git@github.com:luxmeter/markone.git
    $ python setup.py install


## Usage

Markone is a flask app that expect you to specify following environment variables:

* **MARKONE_MD_PATH**: Path to the markdown files
* **MARKONE_OUTPUT_PATH**: Path in which the rendered HTML files will be generated to

Here is an execution example:

    MARKONE_MD_PATH=./example/markdown \
    MARKONE_OUTPUT_PATH=./example/html \
    FLASK_APP=markone.main \
    flask run --port 5000

The app can be than opened under

    http://localhost:5000


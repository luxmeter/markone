# MarkOne

Local web app to render your markdown files.

## Overview

MarkOne is a small web app that is supposed to be run locally
to render your markdown files. This allows you edit your markdown files
in your favorite editor, for example vim.

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

Markone is a flask app that expect you to specify two environment variables:

* **MARKONE_MD_PATH**: Path to the markdown files
* **MARKONE_OUTPUT_PATH**: Path in which the rendered HTML files will be generated to

Here is an execution example:

    MARKONE_MD_PATH=~/notes/markdown \
    MARKONE_OUTPUT_PATH=~/notes/html \
    FLASK_APP=markone.main \
    flask run
    
The app can be than opened under

    http://localhost:5000
    

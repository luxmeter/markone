import json

from flask import render_template, send_from_directory

from markone import logic
from markone.app import app, socketio
from markone.watch import Watch


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tree')
def tree():
    tree = logic.create_tree(app.config['OUTPUT_PATH'])
    return json.dumps(tree)


@app.route('/<path:subpath>')
def watch(subpath):
    if not subpath.endswith('.html'):
        return send_from_directory(app.config['OUTPUT_PATH'], subpath)

    path = app.config['OUTPUT_PATH'] / subpath
    if path.is_file():
        with open(path) as file:
            content = file.read()
        return content
    return 'File does not exist :(', 404


@app.before_first_request
def before_first_request():
    (Watch(app.config['MD_PATH'])
     .observe(logic.gen_html_and_send_update, socketio))

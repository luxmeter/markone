import eventlet

eventlet.monkey_patch()

from markone.watch import Watch

import json
import logging.config
import os
import shutil
from pathlib import Path

import yaml
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from markone import util

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

log = logging.getLogger('markone.app')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tree')
def tree():
    tree = util.create_tree(app.config['OUTPUT_PATH'])
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
     .observe(gen_html_and_send_update))


def gen_html_and_send_update(event):
    logging.debug("sending event")
    shutil.rmtree(app.config['OUTPUT_PATH'], ignore_errors=True)
    util.gen_output(app.config['MD_PATH'], app.config['MD_PATH'], app.config['OUTPUT_PATH'])
    data = util.create_tree(app.config['OUTPUT_PATH'])
    socketio.emit('update_index', data)
    socketio.emit('update_open_file', data)


def main():
    app.logger.handlers.clear()
    with open('logging.yaml', 'r') as f:
        conf = yaml.load(f)
    logging.config.dictConfig(conf)

    config = dict()
    config['MD_PATH'] = (Path('./example/markdown').absolute()
                         if not os.getenv('MARKONE_MD_PATH')
                         else Path(os.getenv('MARKONE_MD_PATH')))
    config['OUTPUT_PATH'] = (Path('./example/html').absolute()
                             if not os.getenv('MARKONE_OUTPUT_PATH')
                             else Path(os.getenv('MARKONE_OUTPUT_PATH')))
    app.config.from_mapping(config)

    setup(config['MD_PATH'], config['OUTPUT_PATH'])


def setup(src_dir: Path, output_dir):
    shutil.rmtree(app.config['OUTPUT_PATH'], ignore_errors=True)
    util.gen_output(src_dir, src_dir, output_dir)


main()
if __name__ == '__main__':
    socketio.run(app)

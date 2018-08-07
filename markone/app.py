import json
import logging.config
import os
import shutil
import threading
import time
from pathlib import Path

import yaml
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from watchdog.observers import Observer

from markone import util
from markone.eventhandler import MarkdownTransformer

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.route('/')
def index():
    context = {
        'md_path': app.config['MD_PATH'],
        'output_path': app.config['OUTPUT_PATH']
    }
    return render_template('index.html', **context)


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
    context = {
        'md_path': app.config['MD_PATH'],
        'output_path': app.config['OUTPUT_PATH']
    }
    watchdog_thread = threading.Thread(name="watchdog", target=watch, kwargs=context)
    watchdog_thread.setDaemon(True)
    watchdog_thread.start()


def watch(md_path, output_path):
    event_handler = MarkdownTransformer(socketio, md_path, output_path)
    observer = Observer()
    observer.schedule(event_handler, str(md_path), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def setup(src_dir: Path, output_dir):
    shutil.rmtree(app.config['OUTPUT_PATH'], ignore_errors=True)
    util.gen_output(src_dir, src_dir, output_dir)


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
    socketio.run(app, debug=True)


if __name__ == '__main__':
    main()

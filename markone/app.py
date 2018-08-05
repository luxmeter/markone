import json
import logging.config
import threading
import time
from pathlib import Path

import yaml
from flask import Flask, render_template
from flask_socketio import SocketIO
from watchdog.observers import Observer

from markone.eventhandler import MarkdownTransformer

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    context = {
        'md_path': app.config['MD_PATH'],
        'output_path': app.config['OUTPUT_PATH']
    }
    return render_template('index.html', **context)


@app.route('/tree')
def tree():
    tree = create_tree(app.config['OUTPUT_PATH'])
    return json.dumps(tree)


@app.route('/watch/<path:subpath>')
def watch(subpath):
    path = app.config['OUTPUT_PATH'] / subpath
    if path.is_file():
        with open(path) as file:
            content = file.read()
        return content
    return 'File does not exist :(', 404


def create_tree(root):
    tree = []
    for path in root.iterdir():
        if path.is_dir():
            tree.append({'text': path.name, 'children': create_tree(path), 'node_type': 'child'})
        else:
            tree.append({'text': path.name, 'icon': 'jstree-file', 'node_type': 'leaf'})
    return tree


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
    observer = Observer()
    observer.schedule(MarkdownTransformer(socketio, output_path), str(md_path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    app.logger.handlers.clear()
    with open('logging.yaml', 'r') as f:
        conf = yaml.load(f)
    logging.config.dictConfig(conf)

    config = dict()
    config['MD_PATH'] = Path('./example/markdown').absolute()
    config['OUTPUT_PATH'] = Path('./example/html').absolute()
    app.config.from_mapping(config)

    socketio.run(app, debug=True)


if __name__ == '__main__':
    main()

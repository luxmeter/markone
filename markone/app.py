import json
import logging.config
import shutil
import threading
import time
from pathlib import Path

import jinja2
import markdown
import pkg_resources
import yaml
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from watchdog.observers import Observer

from markone.eventhandler import MarkdownTransformer

template = pkg_resources.resource_string('markone', '/'.join(('templates', 'watch.html'))).decode('utf-8')

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
    tree = create_tree(app.config['OUTPUT_PATH'])
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


def setup(src_dir: Path, output_dir):
    shutil.rmtree(output_dir, ignore_errors=True)
    gen_output(src_dir, src_dir, output_dir)


def gen_output(root, src_dir, output_dir):
    for input_path in src_dir.iterdir():
        if any(pattern in str(input_path.absolute()) for pattern in ['.DS_Store', '.git']):
            continue
        if input_path.is_dir():
            gen_output(root, input_path, output_dir)
            continue

        relative_path = input_path.relative_to(root)
        if relative_path.suffix == '.md':
            output_path = output_dir / relative_path.parent / (relative_path.stem + '.html')
        else:
            output_path = output_dir / relative_path.parent / relative_path.name

        if not output_path.parent.is_dir():
            output_path.parent.mkdir(parents=True)

        if relative_path.suffix == '.md':
            with open(input_path) as file:
                md_code = file.read()
                content = markdown.markdown(md_code,
                                            extensions=["codehilite", "extra", "smarty"],
                                            output_format="html5")
                html = jinja2.Template(template).render(content=content)
                output_file = open(output_path, "w", encoding="utf-8")
                output_file.write(html)
        else:
            output_path.symlink_to(input_path)


def main():
    app.logger.handlers.clear()
    with open('logging.yaml', 'r') as f:
        conf = yaml.load(f)
    logging.config.dictConfig(conf)

    config = dict()
    config['MD_PATH'] = Path('./example/markdown').absolute()
    config['OUTPUT_PATH'] = Path('./example/html').absolute()
    app.config.from_mapping(config)

    setup(config['MD_PATH'], config['OUTPUT_PATH'])
    socketio.run(app, debug=True)


if __name__ == '__main__':
    main()

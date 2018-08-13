import logging
import shutil

import markdown
import pkg_resources
from jinja2 import Environment, PackageLoader

from markone.app import app

log = logging.getLogger('markone.logic')
template = pkg_resources.resource_string('markone', '/'.join(('templates', 'watch.html'))).decode('utf-8')
env = Environment(
    loader=PackageLoader('markone', 'templates'),
)


def gen_html_and_send_update(event, socketio):
    log.debug(f'directory was updated: {event}')
    shutil.rmtree(app.config['OUTPUT_PATH'], ignore_errors=True)
    gen_output(app.config['MD_PATH'], app.config['MD_PATH'], app.config['OUTPUT_PATH'])
    data = create_tree(app.config['OUTPUT_PATH'])
    socketio.emit('update_index', data)
    socketio.emit('update_open_file', data)
    log.info(f'directory change detected; updates sent to client')


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
                html = env.get_template('watch.html').render(content=content)
                output_file = open(output_path, "w", encoding="utf-8")
                output_file.write(html)
        else:
            output_path.symlink_to(input_path)


def create_tree(root):
    tree = []
    for path in root.iterdir():
        if path.is_dir():
            tree.append({'text': path.name, 'children': create_tree(path), 'node_type': 'child'})
        else:
            tree.append({'text': path.name, 'icon': 'jstree-file', 'node_type': 'leaf'})
    return tree

import logging
import os
import shutil
import sys
from pathlib import Path

from markone.views import *

log = logging.getLogger('markone')

config = dict()
config['MD_PATH'] = (Path('./example/markdown').absolute()
                     if not os.getenv('MARKONE_MD_PATH')
                     else Path(os.getenv('MARKONE_MD_PATH')))
config['OUTPUT_PATH'] = (Path('./example/html').absolute()
                         if not os.getenv('MARKONE_OUTPUT_PATH')
                         else Path(os.getenv('MARKONE_OUTPUT_PATH')))

if (Path(config['OUTPUT_PATH']).absolute().parent == config['MD_PATH'].absolute()
        or Path(config['MD_PATH']).absolute().parent == config['OUTPUT_PATH'].absolute()):
    log.error("MARKONE_MD_PATH must not be parent of MARKONE_OUTPUT_PATH and vice versa")
    sys.exit(1)

app.config.from_mapping(config)

shutil.rmtree(app.config['OUTPUT_PATH'], ignore_errors=True)
logic.gen_output(app.config['MD_PATH'], app.config['MD_PATH'], app.config['OUTPUT_PATH'])

if __name__ == '__main__':
    port = os.getenv('MARKONE_PORT', 5000)
    log.info(f'App started and listens on http://localhost:{port}')
    socketio.run(app, port=port)

import logging.config
import os

import eventlet
import pkg_resources
import yaml

eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

_conf_name = ('logging.yaml'
              if os.getenv('FLASK_ENVIRONMENT', '').lower() != 'development'
              else 'logging-dev.yaml')
logging.config.dictConfig(yaml.load(
    pkg_resources.resource_string('markone', _conf_name).decode('utf-8')))

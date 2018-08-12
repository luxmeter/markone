import logging.config

import eventlet
import pkg_resources
import yaml

eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

app.logger.handlers.clear()
f = pkg_resources.resource_string('markone', 'logging.yaml').decode('utf-8')
conf = yaml.load(f)
logging.config.dictConfig(conf)

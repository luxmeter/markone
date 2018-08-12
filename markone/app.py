import logging.config

import eventlet
import yaml

eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

app.logger.handlers.clear()
with open('logging.yaml', 'r') as f:
    conf = yaml.load(f)
logging.config.dictConfig(conf)

import logging
import sys
import threading

import yaml
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Timer
import json
import sys
import time
from watchdog.observers import Observer

from markone.eventhandler import FileSystemEventHandler
import logging.config



app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    Timer(1, emit_update).start()
    return render_template('index.html')


def emit_update():
    data = json.loads('{"hello": "world"}')
    socketio.emit('update', data)


def watch():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(FileSystemEventHandler(socketio), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    with open('logging.yaml', 'r') as f:
        conf = yaml.load(f)
    logging.config.dictConfig(conf)

    watchdog_thread = threading.Thread(target=watch, name="watchdog")
    watchdog_thread.setDaemon(True)
    watchdog_thread.start()
    socketio.run(app, debug=True)


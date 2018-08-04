import json

import watchdog.events
import logging


log = logging.getLogger('markone.FileSystemEventHandler')
class FileSystemEventHandler(watchdog.events.FileSystemEventHandler):

    def __init__(self, socketio) -> None:
        super().__init__()
        self.socketio = socketio

    def on_modified(self, event):
        log.info("event: " + str(event))
        data = json.loads(f'{{ "path": "hallo" }}')
        self.socketio.emit('messages', f'{{ hello: "{data}" }}')

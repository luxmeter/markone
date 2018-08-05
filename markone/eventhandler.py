import json

import watchdog.events
import logging


log = logging.getLogger('markone.FileSystemEventHandler')
class MarkdownTransformer(watchdog.events.FileSystemEventHandler):

    def __init__(self, socketio, output_path) -> None:
        super().__init__()
        self.socketio = socketio
        self.output_path = output_path

    def on_modified(self, event):
        log.info("event: " + str(event))
        data = json.loads(f'{{ "path": "hallo" }}')
        self.socketio.emit('messages', f'{{ hello: "{data}" }}')

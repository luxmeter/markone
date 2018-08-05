import json
import logging
from pathlib import Path

import arrow
import watchdog.events


class MarkdownTransformer(watchdog.events.FileSystemEventHandler):
    def __init__(self, socketio, output_path) -> None:
        super().__init__()
        self.socketio = socketio
        self.output_path = output_path
        self.last_modified_by_path = dict()
        self.log = logging.getLogger(self.__class__.__name__)

    def already_consumed(self, event):
        path = Path(event.src_path)
        modified_date = arrow.get(path.stat().st_mtime)
        self.log.debug(f'{path} was modified: {modified_date}')
        if path in self.last_modified_by_path:
            self.log.debug(f'path already seen {path}')
            prev_modified_date = self.last_modified_by_path[path]
            if prev_modified_date == modified_date:
                self.log.debug(f'last modified date didn\'t change for {path}')
                return True
        self.last_modified_by_path[path] = modified_date
        return False

    def on_any_event(self, event):
        if not isinstance(event, (watchdog.events.FileCreatedEvent, watchdog.events.FileModifiedEvent)):
            return
        if self.already_consumed(event):
            self.log.debug(f'event already consumed: {event}')
            return
        data = json.loads(f'{{ "path": "hallo" }}')
        self.socketio.emit('messages', f'{{ hello: "{data}" }}')
        self.log.info(f'event consumed: {event}')

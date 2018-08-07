import logging
import shutil
import threading
from time import sleep

import watchdog.events

from markone import util


class MarkdownTransformer(watchdog.events.FileSystemEventHandler):
    def __init__(self, socketio, md_path, output_path) -> None:
        super().__init__()
        self.socketio = socketio
        self.md_path = md_path
        self.output_path = output_path
        self.events_batch = []
        self.log = logging.getLogger(self.__class__.__name__)

        self.lock = threading.Lock()
        timer = threading.Timer(1, self.consume_events)
        timer.daemon = True
        timer.start()

    def consume_events(self):
        while True:
            self.lock.acquire()
            if self.events_batch:
                self.events_batch.clear()
                self.gen_html_and_send_update()
            self.lock.release()
            self.log.debug("Read events batch")
            sleep(0.5)

    def on_any_event(self, event):
        self.log.debug('event:' + str(event))
        self.events_batch.append(event)

    def gen_html_and_send_update(self):
        shutil.rmtree(self.output_path, ignore_errors=True)
        util.gen_output(self.md_path, self.md_path, self.output_path)
        data = util.create_tree(self.output_path)
        self.socketio.emit('update_index', data)
        self.socketio.emit('update_open_file', data)

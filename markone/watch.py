import threading
import time

import arrow


class Watch:
    def __init__(self, dir, delay=1):
        self._delay = delay
        self._dir = dir
        self._thread = None
        self._stop = False

    def stop(self):
        self._stop = True

    def _observe(self, dir, observer, delay, last_tree):
        def missing_files(last_tree, cur_tree):
            missing = []
            for path in cur_tree:
                if path not in last_tree:
                    missing.append(path)
            return missing

        while not self._stop:
            cur_tree = self.generate_tree(dir)

            added_files = missing_files(last_tree, cur_tree)
            removed_files = missing_files(cur_tree, last_tree)

            updated_files = []
            for path, last_stats in last_tree.items():
                if path in cur_tree:
                    cur_stats = cur_tree[path]
                    if last_stats < cur_stats:
                        updated_files.append(path)

            if added_files or removed_files or updated_files:
                observer({
                    'added_files': added_files,
                    'removed_files': removed_files,
                    'updated_files': updated_files
                })
            last_tree = cur_tree
            time.sleep(delay)

    def generate_tree(self, dir):
        cur_tree = {}
        for path in dir.glob('**/*'):
            if path.exists():
                cur_tree[path] = arrow.get(path.stat().st_mtime)
        return cur_tree

    def observe(self, observer):
        if self._thread:
            raise RuntimeError('Already watching')

        # need to generate the tree in main thread
        # in order to observe immediate updates
        last_tree = self.generate_tree(self._dir)
        thread = threading.Thread(name="Spider", target=self._observe,
                                  args=(self._dir, observer, self._delay, last_tree))
        thread.daemon = True
        thread.start()

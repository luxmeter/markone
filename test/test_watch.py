import logging
import os
import shutil
from collections import Counter
from pathlib import Path

import arrow
import pytest

from markone.watch import Watch
from test import util
from .context import configure_logger

configure_logger()
log = logging.getLogger(__name__)


@pytest.fixture()
def dir():
    dir = (Path(__file__).parent / ('watched_dir'))
    if dir.is_dir():
        shutil.rmtree(dir)
    dir.mkdir()
    yield dir
    if dir.is_dir():
        shutil.rmtree(dir)


@util.log()
def test_file_updated(dir):
    counter = Counter()

    def observer(update, counter=counter):
        log.debug(f'Received event: {update}')
        counter.update({
            'added_files': len(update['added_files']),
            'removed_files': len(update['removed_files']),
            'updated_files': len(update['updated_files']),
        })

    path = (dir / 'test-file.txt')
    path.touch()
    t = arrow.now('Europe/Berlin').shift(hours=-1).timestamp
    os.utime(path, (t, t))

    spider = Watch(dir, delay=0.5)
    spider.observe(observer)

    # time.sleep(1)
    path = (dir / 'test-file.txt')
    path.touch()

    try:
        was_triggered(counter, files_updated=1)
    finally:
        spider.stop()


@util.log()
def test_file_removed(dir):
    counter = Counter()

    def observer(update, counter=counter):
        log.debug(f'Received event: {update}')
        counter.update({
            'added_files': len(update['added_files']),
            'removed_files': len(update['removed_files']),
            'updated_files': len(update['updated_files']),
        })

    (dir / 'test-file.txt').touch()

    spider = Watch(dir, delay=0.5)
    spider.observe(observer)

    (dir / 'test-file.txt').unlink()

    try:
        was_triggered(counter, files_removed=1)
    finally:
        spider.stop()


@util.log()
def test_file_added(dir):
    counter = Counter()

    def observer(update, counter=counter):
        log.debug(f'Received event: {update}')
        counter.update({
            'added_files': len(update['added_files']),
            'removed_files': len(update['removed_files']),
            'updated_files': len(update['updated_files']),
        })

    spider = Watch(dir, delay=0.5)
    spider.observe(observer)

    (dir / 'test-file.txt').touch()

    try:
        was_triggered(counter, files_added=1)
    finally:
        spider.stop()


@util.retry(AssertionError, tries=3, delay=1)
def was_triggered(counter, files_added=None, files_removed=None, files_updated=None):
    if files_added:
        assert counter['added_files'] == files_added
    if files_removed:
        assert counter['removed_files'] == files_removed
    if files_updated:
        assert counter['updated_files'] == files_updated

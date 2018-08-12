import logging.config
from pathlib import Path

import yaml


def configure_logger():
    path = (Path(__file__).parent / 'logging.yaml')
    if path:
        with open(path, 'r') as f:
            conf = yaml.load(f)
        logging.config.dictConfig(conf)

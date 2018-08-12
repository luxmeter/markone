import logging.config
import os

import yaml


def configure_logger():
    with open(os.path.join(os.path.dirname(__file__), 'logging.yaml'), 'r') as f:
        conf = yaml.load(f)
    logging.config.dictConfig(conf)

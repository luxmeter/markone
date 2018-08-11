import logging.config
import os
import sys

import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

with open(os.path.join(os.path.dirname(__file__), 'logging.yaml'), 'r') as f:
    conf = yaml.load(f)
logging.config.dictConfig(conf)

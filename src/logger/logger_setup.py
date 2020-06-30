"""
Author:     David Walshe
Date:       04 June 2020
"""


import logging
import logging.config
import yaml
import os

config_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(config_path, 'logger_config.yaml'), 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

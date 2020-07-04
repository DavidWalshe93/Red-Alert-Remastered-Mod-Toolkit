"""
Author:     David Walshe
Date:       04 June 2020
"""


import logging
import logging.config
import yaml
import os

with open(os.environ["RA_LOGGER_CONFIG_PATH"], 'r') as fh:
    config = yaml.safe_load(fh.read())
    logging.config.dictConfig(config)

"""
Author:     David Walshe
Date:       05 July 2020
"""

import os
import json
import logging

from src.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class ConfigManager(metaclass=Singleton):

    def __init__(self):
        """
        Singleton class that holds the user's configuration data.
        """
        self.config = {}

    def read_config(self) -> None:
        """
        Read in the user configuration file.
        """
        if self.config == {}:
            self.force_read_config()

    def force_read_config(self) -> None:
        """
        Reads in the configuration file contents regardless of current config status.
        """
        try:
            with open(os.environ["RA_USER_CONFIG_PATH"], "r") as fh:
                self.config = json.load(fh)
        except FileNotFoundError as err:
            logger.error(f"Cannot read user config file.\n\t{err}")

    def save_config(self):
        """
        Saves the user configuration to the disk.
        """
        if self.config != {}:
            try:
                with open(os.environ["RA_USER_CONFIG_PATH"], "w") as fh:
                    json.dump(self.config, fh, indent=4)
            except OSError as err:
                logger.error(f"Cannot write to user config file.\n\t{err}")

    def get_config(self, key) -> any:
        """
        Helper method that gets an item from the config dictionary depending on the key passed.

        :param key: The config look-up key.
        :return: The value of the key passed.
        """
        self.read_config()
        value = self.config.get(key, None)

        return value

    @property
    def map_directory(self):
        self.read_config()
        return self.get_config("map_directory")

    @map_directory.setter
    def map_directory(self, value):
        if value != "":
            logger.info(f"Saving 'map_directory' as {value}'")
            self.config.update({"map_directory": value})
            self.save_config()

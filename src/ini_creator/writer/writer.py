"""
Author:     David Walshe
Date:       03 July 2020
"""

import os
import logging

from configparser import ConfigParser

from src.db_driver.helpers.db_helper import DBHelper

logger = logging.getLogger(__name__)


class IniWriter:

    FILE_NAME = "output.ini"

    def __init__(self):
        self.model = DBHelper()
        self.writer = ConfigParser(allow_no_value=True)
        self.writer.optionxform = str

    def build(self):
        self.add(self.model.infantry)
        self.add(self.model.buildings)
        self.add(self.model.vehicles)
        self.add(self.model.aircraft)
        self.add(self.model.ships)

        with open(IniWriter.FILE_NAME, "w") as fh:
            self.writer.write(fh)

        logger.info(f".INI file created @ {os.path.join(os.getcwd(), IniWriter.FILE_NAME)}")

    def add(self, data: list):
        for item in data:
            section = item.pop("Tag").replace("[", "").replace("]", "")
            comment = item.pop("Name")

            self.writer.add_section(section)
            self.writer.set(section, f"; {comment}")
            for key, value in item.items():
                try:
                    self.writer.set(section, key, str(value))
                except Exception as err:
                    print(err)
        


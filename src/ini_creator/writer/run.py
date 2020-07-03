"""
Author:     David Walshe
Date:       02 July 2020
"""

from configparser import ConfigParser

from src.db_driver.db_manager import DBManager


class IniWriter:

    def __init__(self):
        self.model = DBManager()
        self.writer = ConfigParser()

    def data_fields(self):
        {
            "buildings": self.model.all()
        }

write_config = ConfigParser()




write_config.add_section("Section1")
write_config.set("Section1", "name", "Jane")

with open("sample.ini", "w") as fh:
    write_config.write(fh)

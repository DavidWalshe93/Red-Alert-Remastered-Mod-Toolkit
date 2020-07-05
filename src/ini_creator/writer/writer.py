"""
Author:     David Walshe
Date:       03 July 2020
"""

import os
import logging

from configparser import ConfigParser

from src.db_driver.helpers.db_helper import DBHelper
from src.config.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class IniWriter:
    NURPLE_POSTFIX = "_nurple_mod.mpr"

    def __init__(self):

        self.model = DBHelper()
        self.writer = ConfigParser(allow_no_value=True)
        self.writer.optionxform = str

    def build(self) -> None:
        """
        High level build command to link and generate mod files.
        """
        self.link()
        self.compile()

    def link(self) -> None:
        """
        Links all the ini sections with the corresponding data.
        """
        self.add(self.model.infantry)
        self.add(self.model.buildings)
        self.add(self.model.vehicles)
        self.add(self.model.aircraft)
        self.add(self.model.ships)

    def add(self, data: list) -> None:
        """
        Creates a sections for use in the ini file and attaches all their associated data.

        :param data: A list of sections and their assoicated data.
        """
        for item in data:
            # Get the meta information
            section = item.pop("Tag").replace("[", "").replace("]", "")
            comment = item.pop("Name")

            # Add the section
            self.writer.add_section(section)
            # Add the comment
            self.writer.set(section, f"; {comment}")

            # Add all the associated data.
            for key, value in item.items():
                try:
                    self.writer.set(section, key, str(value))
                except Exception as err:
                    logger.error(f"{err}")

    def compile(self):
        for mpr_file in self.mpr_files:
            out_file = mpr_file.replace(".mpr", "")

            with open(mpr_file, "r") as fh:
                mpr_content = fh.read()

            out_file = f"{out_file}{self.NURPLE_POSTFIX}"
            with open(out_file, "w") as fh:
                # Add Mods
                self.writer.write(fh)
                # Add map content
                fh.write(mpr_content)

                logger.info(f"Created modded mpr file @ {out_file}")

    @property
    def mpr_files(self) -> list:
        """
        Get all the mpr file paths to use for the mod adding.

        :return: A list of file paths for .mpr files in the chosen map directory.
        """
        try:
            map_dir = ConfigManager().map_directory
            mpr_files = os.listdir(map_dir)
            mpr_files = [os.path.join(map_dir, file) for file in mpr_files if file.endswith(".mpr")]
            mpr_files = [file for file in mpr_files if file.find(self.NURPLE_POSTFIX) == -1]

            return mpr_files
        except OSError as err:
            logger.error(f"Could not get map directory contents.\n\t"
                         f"User config: {ConfigManager().config}\n\t"
                         f"{err}")

            return []

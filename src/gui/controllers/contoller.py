"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
import logging

from PyQt5 import QtWidgets, QtGui

from src.ini_creator.writer.writer import IniWriter
from src.db_driver.db_manager import DBManager
from src.config.config_manager import ConfigManager

if TYPE_CHECKING:
    from src.gui.gui import MainWindow

logger = logging.getLogger(__name__)


class Controller(ABC):

    def __init__(self, view: MainWindow):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        :param db: The database to access.
        """
        self.view = view
        self.model = DBManager()
        self.config_manager = ConfigManager()

        self.compile_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+C'), self.view)

    @abstractmethod
    def bind_slots(self) -> None:
        """
        Abstract method used to bind slots in the view.
        """
        self.view.actionCompile.triggered.connect(self.compile)

    @abstractmethod
    def bind_shortcuts(self) -> None:
        """
        Abstract method used to bind shortcuts to the view.
        """
        self.compile_shortcut.activated.connect(self.compile)

    def compile(self):
        """
        Compiles current data in the database into an ini file for use in Red Alert.
        """
        if self.config_manager.map_directory is None:
            self.showDialog()
        try:
            logger.info("Compiling mods...")
            ini_writer = IniWriter()
            ini_writer.build()
            logger.info("Mod files compiled")
        except Exception as err:
            print(err)

    @abstractmethod
    def populate_data(self, result: any) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass

    def showDialog(self) -> None:
        """
        Show dialog for selecting mod map directory.
        """
        try:
            home_dir = self.config_manager.map_directory
            dir_name = QtWidgets.QFileDialog.getExistingDirectory(self.view, "Select map dir", home_dir)
            self.config_manager.map_directory = dir_name
        except Exception as err:
            logger.info(f"Map Directory Dialog Error\n\t"
                        f"{err}")

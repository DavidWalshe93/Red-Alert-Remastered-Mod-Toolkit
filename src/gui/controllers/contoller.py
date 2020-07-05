"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

from PyQt5 import QtWidgets, QtGui

from src.ini_creator.writer.writer import IniWriter
from src.db_driver.db_manager import DBManager

if TYPE_CHECKING:
    from src.gui.gui import MainWindow


class Controller(ABC):

    def __init__(self, view: MainWindow):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        :param db: The database to access.
        """
        self.view = view
        self.model = DBManager()

        self.compile_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+C'), self.view)

    @abstractmethod
    def bind_slots(self) -> None:
        """
        Abstract method used to bind slots in the view.
        """
        # Bindings
        self.view.actionCompile.triggered.connect(self.compile)

        # Hotkeys
        self.compile_shortcut.activated.connect(self.compile)

    def compile(self):
        """
        Compiles current data in the database into an ini file for use in Red Alert.
        """
        self.showDialog()
        try:
            ini_writer = IniWriter()
            ini_writer.build()
        except Exception as err:
            print(err)

    @abstractmethod
    def populate_data(self, result: any) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass

    def showDialog(self):
        try:
            from pathlib import Path
            from src.config.config_manager import ConfigManager
            home_dir = ConfigManager().map_directory
            print(home_dir)
            dir_name = QtWidgets.QFileDialog.getExistingDirectory(self.view, "Select map dir", home_dir)
            ConfigManager().map_directory = dir_name
            # if fname[0]:
            #     f = open(fname[0], 'r')
            #
            #     with f:
            #         data = f.read()
            #         print(data)
        except Exception as err:
            print(err)



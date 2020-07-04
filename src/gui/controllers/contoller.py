"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

from PyQt5 import QtWidgets, QtGui

from src.db_driver.db_helper import DBHelper
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
        try:
            ini_writer = IniWriter()
            ini_writer.build()
            # db_helper = DBHelper()
            #
            # print(db_helper.infantry)
        except Exception as err:
            print(err)

    @abstractmethod
    def populate_data(self, result: any) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass



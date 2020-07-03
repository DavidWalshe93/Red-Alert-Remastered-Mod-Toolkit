"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
from src.db_driver.db_helper import DBHelper

if TYPE_CHECKING:
    from src.gui.gui import MainWindow
    from src.db_driver.db_manager import DBManager


class Controller(ABC):

    def __init__(self, view: MainWindow, model: DBManager):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        :param db: The database to access.
        """
        self.view = view
        self.model = model

    @abstractmethod
    def bind_slots(self) -> None:
        """
        Abstract method used to bind slots in the view.
        """
        self.view.actionCompile.triggered.connect(self.compile)

    def compile(self):
        try:
            db_helper = DBHelper()
            print(db_helper.infantry)
        except Exception as err:
            print(err)

    @abstractmethod
    def populate_data(self, result: any) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass



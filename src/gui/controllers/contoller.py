"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.gui.gui import MainWindow
    from src.db_driver.db_manager import DBManager


class Controller(ABC):

    def __init__(self, view: MainWindow, db: DBManager):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        :param db: The database to access.
        """
        self.view = view
        self.db = db

    @abstractmethod
    def bind_slots(self):
        """
        Abstract method used to bind slots in the view.
        """
        pass

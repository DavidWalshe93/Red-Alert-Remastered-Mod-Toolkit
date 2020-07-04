"""
Author:     David Walshe
Date:       04 July 2020
"""

from PyQt5.QtWidgets import QMainWindow
from src.gui.view.core.app import Ui_MainWindow


class View(Ui_MainWindow, QMainWindow):

    def __init__(self, *args, **kwargs):
        """
        Abstract base for all views in the application.
        """
        super().__init__(*args, **kwargs)

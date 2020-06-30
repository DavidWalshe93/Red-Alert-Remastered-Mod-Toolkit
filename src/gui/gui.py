"""
Author:     David Walshe
Date:       29 June 2020
"""

import src.logger.logger_setup
import logging

logger = logging.getLogger(__name__)

import sys
from os import environ
from pprint import pprint

environ["RA_DB_LOCATION"] = "../../db/defaults.db"

from PyQt5 import QtWidgets
from src.gui.base.app import Ui_MainWindow
from src.db_driver.db_manager import DBManager
from src.gui.controllers.unit import UnitController


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.update()
    db = DBManager()
    unit_controller = UnitController(window, db)
    unit_controller.bind_slots()
    app.exec_()


if __name__ == '__main__':

    run()


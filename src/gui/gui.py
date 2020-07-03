"""
Author:     David Walshe
Date:       29 June 2020
"""

import logging

import src.logger.logger_setup

logger = logging.getLogger(__name__)

import sys
from os import environ

environ["RA_DB_LOCATION"] = "../../db/defaults.db"

from PyQt5 import QtWidgets
from src.db_driver.db_manager import DBManager
from src.gui.controllers.unit.core import UnitCoreController
from src.gui.view.app import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.update()
    db = DBManager()
    unit_controller = UnitCoreController(window, db)
    unit_controller.bind_slots()
    app.exec_()


if __name__ == '__main__':

    run()


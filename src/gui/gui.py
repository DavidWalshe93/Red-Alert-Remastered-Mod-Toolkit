"""
Author:     David Walshe
Date:       29 June 2020
"""

import logging
import sys

from PyQt5 import QtWidgets

from src.db_driver.db_manager import DBManager
from src.gui.controllers.unit.core import UnitCoreController
from src.gui.view.app import MainWindow


def run():
    logger.info(f"=" * 100)
    logger.info("Application launched")

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Setup controllers with view.
    unit_controller = UnitCoreController(window)
    unit_controller.bind_slots()

    app.exec_()

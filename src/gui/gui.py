"""
Author:     David Walshe
Date:       29 June 2020
"""

import logging
import sys

from PyQt5 import QtWidgets

from src.db_driver.db_manager import DBManager
from src.gui.controllers.unit.unit_structure import UnitStructureController
from src.gui.view.app import MainWindow

logger = logging.getLogger(__name__)


def run():
    try:
        logger.info(f"=" * 100)
        logger.info("Application launched")
    
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
    
        # Setup controllers with view.
        unit_controller = UnitStructureController(window)
        unit_controller.bind_slots()
        unit_controller.bind_shortcuts()
    
        app.exec_()
    except Exception as err:
        logger.error(f"{err}")
        raise err

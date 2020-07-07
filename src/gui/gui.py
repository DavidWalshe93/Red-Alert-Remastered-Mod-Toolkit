"""
Author:     David Walshe
Date:       29 June 2020
"""

import logging
import sys

from PyQt5 import QtWidgets

from src.db_driver.db_manager import DBManager
from src.gui.controllers.app_controller import AppController
from src.gui.controllers.unit.unit_structure import UnitStructureController
from src.gui.controllers.general.general import GeneralController
from src.gui.view.app import MainWindow

logger = logging.getLogger(__name__)


def run():
    # try:
    logger.info(f"=" * 100)
    logger.info("Application launched")
        #
        # app = QtWidgets.QApplication(sys.argv)
        # window = MainWindow()
        # window.show()

        # Setup controllers with view.
    controller = AppController()
    controller.run()
        # unit_structure_controller = UnitStructureController(window)
        # general_controller = GeneralController(window)
    
    #     app.exec_()
    # except Exception as err:
    #     logger.error(f"{err}")
    #     raise err

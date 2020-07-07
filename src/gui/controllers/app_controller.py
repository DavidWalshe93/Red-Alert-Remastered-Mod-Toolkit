"""
Author:     David Walshe
Date:       07 July 2020
"""

import logging

from PyQt5 import QtWidgets
from PyQt5 import QtGui

# Model
from src.db_driver.db_manager import DBManager
# View
from src.gui.view.app import MainWindow
# Controllers
from src.gui.controllers.unit.unit_structure import UnitStructureController
from src.gui.controllers.general.general import GeneralController

logger = logging.getLogger(__name__)


class AppController:

    def __init__(self):
        self.view = None
        self.model = None
        self.controllers = []

        self.compile_shortcut = None
        self.save_shortcut = None

    def bind_controller_slots(self) -> None:
        """
        Abstract method used to bind slots in the view.
        """
        print("slots")
        self.view.actionCompile.triggered.connect(self.compile)

    def bind_controller_shortcuts(self) -> None:
        """
        Abstract method used to bind shortcuts to the view.
        """
        self.compile_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Alt+C'), self.view)
        self.compile_shortcut.activated.connect(self.compile)

        self.save_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+S'), self.view)
        self.save_shortcut.activated.connect(self.save)

    def save(self):
        logger.info(f"Saving data")
        for controller in self.controllers:
            controller.update_model()

    def compile(self):
        """
        Compiles current data in the database into an ini file for use in Red Alert.
        """
        logger.info(f"Compiling mods")
        # if self.config_manager.map_directory is None:
        #     self.showDialog()
        # try:
        #     logger.info("Compiling mods...")
        #     ini_writer = IniWriter()
        #     ini_writer.build()
        #     logger.info("Mod files compiled")
        # except Exception as err:
        #     print(err)

    def populate_data(self) -> None:
        for controller in self.controllers:
            controller.populate_data()

    @staticmethod
    def create_view():
        view = MainWindow()
        view.show()

        return view

    @staticmethod
    def create_model():
        db = DBManager()

        return db

    @staticmethod
    def create_controllers(view: MainWindow, model: DBManager) -> list:
        controllers_classes = []

        controllers_classes.append(GeneralController)
        controllers_classes.append(UnitStructureController)

        controllers = []
        for _class in controllers_classes:
            controllers.append(_class(view, model))

        return controllers

    def run(self):
        try:
            app = QtWidgets.QApplication([])
            self.view = self.create_view()
            self.model = self.create_model()
            self.controllers = self.create_controllers(self.view, self.model)

            for controller in self.controllers:
                controller.populate_data()

            self.bind_controller_slots()
            self.bind_controller_shortcuts()

            app.exec_()
        except Exception as err:
            logger.error(f"{err}")
            raise err

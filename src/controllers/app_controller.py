"""
Author:     David Walshe
Date:       07 July 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import logging
import functools
import os

from typing import Union

from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QCheckBox, QComboBox, QShortcut, QApplication, QWidget, \
    QFileDialog
from PyQt5 import QtGui

# Model
from src.model.db_manager import DBManager
# View
from src.view.app import MainWindow
# Controllers
from src.controllers.unit.unit_structure import UnitStructureController
from src.controllers.general.general import GeneralController

# Decorator helper
from src.utils.decorators import composed

# Database reset functions
from src.model.db_utils import reset_database

# Config_manager
from src.config.config_manager import ConfigManager

# MPR compiler
from src.compiler.compiler import Compiler

if TYPE_CHECKING:
    from src.controllers.controller import Controller

WidgetType = Union[QDoubleSpinBox, QSpinBox, QCheckBox, QComboBox]

logger = logging.getLogger(__name__)


def inject_model_data(method: callable):
    """
    Processes a sender signal and breaks out all relevant information to
    update the database on a widget state change.

    :param method: Method to decorate.
    :return: Decorated method.
    """

    @functools.wraps(method)
    def wrapper(self):
        ret = None

        sender = self.view.sender()
        column = self.get_column(sender)
        widget_name = sender.objectName()
        try:
            attribute = sender.property("property_name")
            controller = self.get_controller(attribute)

            ret = method(self, column, controller, widget_name)

        except AttributeError as err:
            logger.error(f"'property_name' does not exist or is incorrect for {widget_name}")
            logger.error(f"{err}")
        except Exception as err:
            logger.error(f"Error in 'update_db_on_change()' call with {widget_name}")
            logger.error(f"{err}")
            raise err

        return ret

    return wrapper


def inject_table_objects(method: callable) -> callable:
    """
    Injects a the default and custom databases into a methods parameter list.

    :param method: Method to decorate.
    :return: Decorated method.
    """

    @functools.wraps(method)
    def wrapper(self, controller, column, *args, **kwargs):
        try:
            default_table, custom_table = controller.tables

            # Get results for current selected unit name.
            default = self.model.query_first(default_table, Name=controller.name)
            custom = self.model.query_first(custom_table, Name=controller.name)

            key = column.lower()
            if key in custom.inv_mapping_keys():
                column = custom.inverse_mapping()[key]

            ret = method(self, default, custom, column, *args, **kwargs)

            return ret

        except Exception as err:
            logger.error(f"Can't get current data - {err} - locals: {locals()}")
            raise

    return wrapper


def inject_table_dicts(method: callable) -> callable:
    """
    Converts a table object into a dictionary. Used in par with "inject_table_objects".

    :param method: Method to decorate.
    :return: Decorated method.
    """

    @functools.wraps(method)
    def wrapper(self, default, custom, *args, **kwargs):
        default_dict = default.__dict__
        custom_dict = custom.__dict__

        ret = method(self, default_dict, custom_dict, *args, **kwargs)

        return ret

    return wrapper


def remove_sa_instance_state(method: callable) -> callable:
    """
    Strips the database instance fields from the tables before returning them.

    :param method: Method to decorate.
    :return: Decorated method.
    """

    @functools.wraps(method)
    def wrapper(self, default, custom, *args, **kwargs):
        # Remove non-important fields from dict before comparison.
        default.__dict__.pop("_sa_instance_state")
        custom.__dict__.pop("_sa_instance_state")

        ret = method(self, default, custom, *args, **kwargs)

        return ret

    return wrapper


class AppController:

    def __init__(self):
        """
        Main controller for the application.
        """
        self.view = None
        self.model = None
        self.controllers = []

        self.compile_shortcut = None
        self.save_shortcut = None
        self.config_manager = ConfigManager()

        self.exclusion_widgets = [
            "unitComboBox",
            "unitTypeComboBox"
        ]

    @staticmethod
    def create_view() -> MainWindow:
        """
        Creates a view object for the application.

        :return: The created view object.
        """
        view = MainWindow()
        view.show()

        return view

    @staticmethod
    def create_model() -> DBManager:
        """
        Creates a DBManager object for the application.

        :return: The created DBManager object.
        """
        db = DBManager()

        return db

    def bind_controller_slots(self) -> None:
        """
        Used to bind slots in the view.
        """
        logger.info(f"Registering Qt Slots...")
        self.view.actionCompile.triggered.connect(self.compile)
        self.view.actionResetDatabase.triggered.connect(reset_database)
        self.view.actionSelectMapFolder.triggered.connect(self.select_map_dialog)
        self.bind_auto_save()
        logger.info(f"Qt Slots Registered.")

    def bind_controller_shortcuts(self) -> None:
        """
        Used to bind shortcuts to the view.
        """
        logger.info(f"Registering Qt Shortcuts...")
        self.compile_shortcut = QShortcut(QtGui.QKeySequence('Alt+C'), self.view)
        self.compile_shortcut.activated.connect(self.compile)
        logger.info(f"Qt Shortcuts Registered.")

    def select_map_dialog(self) -> None:
        """
        Show dialog for selecting mod map directory.
        """
        dir_name = self.select_directory_dialog("Select RA Map Directory", self.config_manager.map_directory)
        self.config_manager.map_directory = dir_name

    def select_directory_dialog(self, title: str, base_dir: str):
        """
        Opens a Dialog to select a filesystem directory and returns the directory path selected.

        :param title: The title for the directory select dialog.
        :param base_dir: The dir to open the dialog in initially.
        :return: The user selected directory.
        """
        try:
            return QFileDialog.getExistingDirectory(self.view, title, base_dir)
        except Exception as err:
            logger.error(f"Directory Selection Dialog Error\n\t"
                         f"{err}")

    def compile(self):
        """
        Compiles current data in the database into an ini file for use in Red Alert.
        """
        logger.info(f"Compiling mods")
        compiler = Compiler(self.model, self.config_manager.map_directory)
        compiler.compile()

    def populate_data(self) -> None:
        """
        Runs through all controllers of the application anc populates the data into their controlled fields.
        """
        for controller in self.controllers:
            controller.populate_data()

    @staticmethod
    def create_controllers(view: MainWindow, model: DBManager) -> list:
        """
        Creates and adds all sub controllers to the application.

        :param view: The view for the application.
        :param model: The model for the application.
        :return: A list of controllers.
        """
        controllers_classes = []

        controllers_classes.append(GeneralController)
        controllers_classes.append(UnitStructureController)

        controllers = []
        for _class in controllers_classes:
            controllers.append(_class(view, model))

        return controllers

    def bind_auto_save(self):
        """
        Attaches a callback to all data specific widget so on a value change, the data is wrote to the database.
        """
        # for all widgets in the view.
        for attrib_name in dir(self.view):
            # Exclude some non-data specific widgets.
            if attrib_name not in self.exclusion_widgets:
                attrib = self.view.__getattribute__(attrib_name)
                if isinstance(attrib, QDoubleSpinBox):
                    self.view.__getattribute__(attrib_name).valueChanged.connect(self.update_model_on_change)
                elif isinstance(attrib, QSpinBox):
                    self.view.__getattribute__(attrib_name).valueChanged.connect(self.update_model_on_change)
                elif isinstance(attrib, QCheckBox):
                    self.view.__getattribute__(attrib_name).stateChanged.connect(self.update_model_on_change)
                elif isinstance(attrib, QComboBox):
                    self.view.__getattribute__(attrib_name).currentTextChanged.connect(self.update_model_on_change)

    @inject_model_data
    def update_model_on_change(self, column, controller, widget_name) -> None:
        """
        Updated the view and model(DB) when a widget change occurs.

        :param column: The column to change in the data.
        :param controller: The controller to use for the transaction.
        :param widget_name: The name of the widget that changed.
        """
        self.update_model(column, controller)
        self.update_view(controller, column, widget_name)

    def update_model(self, column: str, controller: Controller) -> None:
        """
        Updates the model after a widget change.

        :param column: The column to change.
        :param controller: The controller responsible for the widget.
        """
        if type(controller.value) is float:
            value = round(controller.value, 2)
        else:
            value = controller.value

        try:
            result = self.model.query_first(controller.table, Name=controller.name)

            result.__setattr__(column, value)

            self.model.update(result)
            logger.info(f"Saved: {column} [{value}]")
        except Exception as err:
            logger.error(f"Model Update error for {column} [{value}] - {err}")

    @composed(inject_table_objects, remove_sa_instance_state, inject_table_dicts)
    def update_view(self, default, custom, column, widget_name) -> None:
        """
        Updates the view after a widget change.
        :param default: The default value in the Model.
        :param custom: The custom value in the Model.
        :param column: The column being looked at.
        :param widget_name: The name of the widget to update.
        """
        if default[column] != custom[column]:
            self.view.set_custom_view(widget_name)
        else:
            self.view.set_default_view(widget_name)

    @staticmethod
    def get_column(sender: QWidget):
        """
        Helper method to get the name of a column from its widgets object name.

        :param sender: The sender widget, where the signal came from.
        :return: The name of the column to get data from.
        """
        widget_suffices = ["DoubleSpinBox", "SpinBox", "CheckBox", "ComboBox"]
        obj_name = sender.objectName()

        # Remove the suffices from the widget name.
        for widget in widget_suffices:
            obj_name = obj_name.replace(widget, "")

        # Get the column name.
        column = f"{obj_name[0].upper()}{obj_name[1:]}"

        return column

    def get_controller(self, attribute: str) -> tuple:
        """
        Gets the a controller object that has the property value required or

        :param attribute: The attribute to check exists on the controllers.
        :return: The controller with the desired attribute.
        :raises AttributeError: When the passed attribute doesnt exist on any controller.
        """
        for controller in self.controllers:
            if hasattr(controller, attribute):
                controller.value = attribute
                return controller

        raise AttributeError(f"{attribute} does not exist for any controller objects")

    def run(self):
        """
        Entry point for application.
        """
        try:
            app = QApplication([])
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

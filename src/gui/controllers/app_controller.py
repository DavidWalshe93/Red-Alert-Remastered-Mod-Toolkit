"""
Author:     David Walshe
Date:       07 July 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import logging
import functools

from typing import Union

from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QCheckBox, QComboBox, QShortcut, QApplication, QWidget
from PyQt5 import QtGui

# Model
from src.db_driver.db_manager import DBManager
# View
from src.gui.view.app import MainWindow
# Controllers
from src.gui.controllers.unit.unit_structure import UnitStructureController
from src.gui.controllers.general.general import GeneralController

# Decorator helper
from src.utils.decorators import composed

if TYPE_CHECKING:
    from src.gui.controllers.controller import Controller

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
        self.view = None
        self.model = None
        self.controllers = []

        self.compile_shortcut = None
        self.save_shortcut = None

        self.exclusion_widgets = [
            "unitComboBox",
            "unitTypeComboBox"
        ]

    def bind_controller_slots(self) -> None:
        """
        Abstract method used to bind slots in the view.
        """
        self.view.actionCompile.triggered.connect(self.compile)
        self.bind_auto_save()
        logger.info(f"Registered Qt Slots")

    def bind_controller_shortcuts(self) -> None:
        """
        Abstract method used to bind shortcuts to the view.
        """
        self.compile_shortcut = QShortcut(QtGui.QKeySequence('Alt+C'), self.view)
        self.compile_shortcut.activated.connect(self.compile)
        logger.info(f"Registered Qt Shortcuts")

    # def save(self):
    #     logger.info(f"Saving data")
    #     for controller in self.controllers:
    #         controller.update_model()

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

    def bind_auto_save(self):
        for attrib_name in dir(self.view):
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

    def update_model(self, column: str, controller: Controller):
        try:
            result = self.model.query_first(controller.table, Name=controller.name)

            result.__setattr__(column, controller.value)

            self.model.update(result)
            logger.info(f"Saved: {column} [{controller.value}]")
        except Exception as err:
            logger.error(f"Model Update error - {err}")

    @composed(inject_table_objects, remove_sa_instance_state, inject_table_dicts)
    def update_view(self, default, custom, column, widget_name):
        if default[column] != custom[column]:
            self.view.set_custom_view(widget_name)
        else:
            self.view.set_default_view(widget_name)

    @inject_model_data
    def update_model_on_change(self, column, controller, widget_name):
        self.update_model(column, controller)
        self.update_view(controller, column, widget_name)

    @staticmethod
    def get_column(sender: QWidget):
        widget_suffices = ["SpinBox", "CheckBox", "ComboBox"]
        obj_name = sender.objectName()
        for widget in widget_suffices:
            obj_name = obj_name.replace(widget, "")

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
        try:
            app = QApplication([])
            self.view = self.create_view()
            self.model = self.create_model()
            self.controllers = self.create_controllers(self.view, self.model)

            for controller in self.controllers:
                controller.populate_data()

            self.bind_controller_slots()
            self.bind_controller_shortcuts()

            # db_differ = DbDiff(self.model)

            app.exec_()
        except Exception as err:
            logger.error(f"{err}")
            raise err


class DbDiff:

    def __init__(self, model):
        self.model = model
        self._tables = None

    def tables(self) -> list:
        """
        Lazy init property, gets the table names of the database.

        :return: List of the DB table names.
        """
        if self._tables is None:

            tables = set("_".join(self.model.tables().keys()).split("_"))

            remove_list = ["custom", "default"]
            for item in remove_list:
                try:
                    tables.remove(item)
                except KeyError:
                    pass

            self._tables = list(tables)

        return self._tables

    def check_custom_vs_defaults(self, default_table, custom_table) -> list:
        """
        Checks the custom vs the default_table dictionary to see if they are different.

        :return: The names of the items that are different.
        """
        default_table, custom_table = self.get_current_data(remove_instance_data=True)

        names = []

        # XOR operation to keep only elements that are different.
        unmatched_item = set(default_table.__dict__.items()) ^ set(custom_table.__dict__.items())

        # If there is a difference.
        if len(unmatched_item):
            # Get the name of the feature that is different.
            for item in unmatched_item:
                names.append(item[0])

        return list(set(names))

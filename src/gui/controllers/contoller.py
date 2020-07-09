"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
import logging
import functools

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QCheckBox, QComboBox

from src.ini_creator.writer.writer import IniWriter
from src.db_driver.db_manager import DBManager
from src.config.config_manager import ConfigManager

if TYPE_CHECKING:
    from src.gui.gui import MainWindow


logger = logging.getLogger(__name__)


def non_none_return_value(func: callable) -> callable:
    """
    Wraps a function in a check to see if the function returns non-None value. If None, raise an error.

    :raise ValueError: If the return value is None.
    :return: The wrapped function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return_value = func(*args, **kwargs)

        if return_value is None:
            logger.error(f"None value is not allowed for {func} with *args {args} and **kwargs {kwargs}")
            raise ValueError("None value is not allowed here")

        return return_value

    return wrapper


class Controller(ABC):

    def __init__(self, view: MainWindow, model: DBManager):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        """
        self.view = view
        self.model = model
        self.config_manager = ConfigManager()

    @abstractmethod
    def populate_data(self, result: any = None) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass

    @abstractmethod
    @non_none_return_value
    def get_custom_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        pass

    @abstractmethod
    @non_none_return_value
    def get_default_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        pass

    # def update_model(self) -> None:
    #     """
    #     Saves the current data on the view to the database.
    #     """
    #     try:
    #         # Query the database for the current selected item.
    #         result = self.model.query_first(self.table, Name=self.name)
    #         # Get the property names associate with the item.
    #         name_mapping = self.table.property_names()
    #
    #         self.update_result(result, name_mapping)
    #
    #         # Pass the result back to be updated in the database.
    #         self.model.update(result)
    #
    #         logger.info(f"Successfully updated '{self.name}'")
    #
    #         # Highlight values that differ from the default.
    #         # self.show_difference_highlighting()
    #
    #     except Exception as err:
    #         logger.error(f"Could not update model item '{self.name}' - {err}")
    #         raise
    #
    # def update_result(self, result, name_mapping: dict):
    #     """
    #     Updates each element of the database item with the values of the GUI.
    #
    #     :param result: The database query result.
    #     :param name_mapping: The name mapping of property names.
    #     :return: The update result.
    #     """
    #     for column_name, property_name in name_mapping.items():
    #
    #         if column_name not in ["Id", "Tag"]:
    #             try:
    #                 # Set the attributes of the result to the current selected states of the GUI.
    #                 result.__setattr__(column_name, self.__getattribute__(property_name))
    #
    #             except Exception as err:
    #                 raise err
    #
    #     return result
    #
    # def show_difference_highlighting(self):
    #     """
    #     Update the view to show the difference between defaults and custom settings.
    #     """
    #     label_names = self.get_label_names()
    #     names = self.check_custom_vs_defaults()
    #     self.view.show_differences(label_names, names)
    #
    # def get_label_names(self) -> dict:
    #     """
    #     Gets a list of property names matching the table fields. Removes non GUI related fields.
    #
    #     :return: A dict of property label names.
    #     """
    #     label_names: dict = self.table.property_names()
    #
    #     # Remove non GUI related fields
    #     label_names.pop("Id")
    #     label_names.pop("Name")
    #     label_names.pop("Tag")
    #
    #     return label_names
    #

    #
    # def get_tables(self) -> tuple:
    #     """
    #     Returns the the default and custom table to query data off.
    #
    #     :return: The default and custom table objects.
    #     """
    #     try:
    #         default_table = self.get_defaults_table(self.table_selection)
    #         custom_table = self.get_custom_table(self.table_selection)
    #
    #         return default_table, custom_table
    #     except Exception as err:
    #         logger.error(f"Could not retrieve table data - {err}")
    #
    # def set_defaults(self) -> None:
    #     """
    #     Resets the view and custom model back to defaults.
    #     """
    #     names = self.check_custom_vs_defaults()
    #     try:
    #         default, custom = self.get_current_data()
    #         for name in names:
    #             custom.__setattr__(name, default.__getattribute__(name))
    #
    #         # Persist the defaults to the custom database.
    #         self.model.update(custom)
    #         self.populate_data()
    #         self.update_model()
    #     except Exception as err:
    #         logger.error(f"{err}")
    #


    def showDialog(self) -> None:
        """
        Show dialog for selecting mod map directory.
        """
        try:
            home_dir = self.config_manager.map_directory
            dir_name = QtWidgets.QFileDialog.getExistingDirectory(self.view, "Select map dir", home_dir)
            self.config_manager.map_directory = dir_name
        except Exception as err:
            logger.info(f"Map Directory Dialog Error\n\t"
                        f"{err}")

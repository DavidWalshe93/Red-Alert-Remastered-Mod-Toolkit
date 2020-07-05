"""
Author:     David Walshe
Date:       29 June 2020
"""

import functools
import logging
from typing import Union

from PyQt5 import QtWidgets, QtCore, QtGui

from src.gui.controllers.unit.vehicles import VehiclesController
from src.gui.controllers.unit.infantry import InfantryController
from src.gui.controllers.unit.buildings import BuildingsController

from src.db_driver.models.units.buildings import BuildingsDefault, BuildingsCustom
from src.db_driver.models.units.aircraft import AircraftDefault, AircraftCustom
from src.db_driver.models.units.infantry import InfantryDefault, InfantryCustom
from src.db_driver.models.units.ships import ShipsDefault, ShipsCustom
from src.db_driver.models.units.vehicles import VehiclesDefault, VehiclesCustom

from src.gui.controllers.utils import set_checked, is_checked

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


class UnitStructureController(VehiclesController, InfantryController, BuildingsController):

    def __init__(self, *args, **kwargs):
        """
        Controls updates to the GUI elements via the database.
        """
        super().__init__(*args, **kwargs)
        self.table = None
        self.populate_units_based_on_type()
        self.populate_data()

        self.shortcut_open = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+S'), self.view)

    def bind_slots(self) -> None:
        """
        Method to bind GUI actions to method callbacks.
        """
        super().bind_slots()
        self.view.unitTypeComboBox.currentTextChanged.connect(self.populate_units_based_on_type)
        self.view.unitComboBox.currentTextChanged.connect(self.populate_data)
        self.view.c4checkBox.stateChanged.connect(self.view.c4_adjust_dependencies)
        self.view.saveButton.clicked.connect(self.update_model)
        self.view.defaultsButton.clicked.connect(self.set_defaults)

    def bind_shortcuts(self) -> None:
        """
        Bind all shortcut hot-keys to the GUI.
        """
        super().bind_shortcuts()
        self.shortcut_open.activated.connect(self.update_model)

    def populate_units_based_on_type(self) -> None:
        """
        Populates the units field in the GUI.
        """
        # Get the table selected.
        key = self.type_selection
        self.table = self.get_custom_table(key)

        # Update the combobox with the fields associated with the table selected.
        items = self.model.all_ordered_by(self.table, self.table.Name)
        self.view.unitComboBox.clear()
        for i in items:
            self.view.unitComboBox.addItem(i.Name)

        # Update the view options based on the current state.
        self.view.update_options(key)

    def update_model(self) -> None:
        """
        Saves the current data on the view to the database.
        """
        try:
            # Query the database for the current selected item.
            result = self.model.query_first(self.table, Name=self.name)
            # Get the property names associate with the item.
            name_mapping: dict = self.table.property_names()

            for column_name, property_name in name_mapping.items():
                if column_name not in ["Id", "Tag"]:
                    try:
                        # Set the attributes of the result to the current selected states of the GUI.
                        result.__setattr__(column_name, self.__getattribute__(property_name))
                    except Exception as err:
                        raise err

            # Pass the result back to be updated in the database.
            self.model.update(result)

            logger.info(f"Successfully updated '{self.name}'")

            # Highlight values that differ from the default.
            self.show_difference_highlighting()

        except Exception as err:
            logger.error(f"Could not update model item '{self.name}' - {err}")

    def show_difference_highlighting(self):
        """
        Update the view to show the difference between defaults and custom settings.
        """
        names = self.check_custom_vs_defaults()
        label_names = self.__get_label_names()
        self.view.show_differences(label_names, names)

    def __get_label_names(self) -> dict:
        """
        Gets a list of property names matching the table fields. Removes non GUI related fields.

        :return: A dict of property label names.
        """
        label_names: dict = self.table.property_names()

        # Remove non GUI related fields
        label_names.pop("Id")
        label_names.pop("Name")
        label_names.pop("Tag")

        # Adjust naming for some fields.
        label_names.update({"rot": label_names.pop("ROT")})

        return label_names

    def get_current_data(self, remove_instance_data: bool = False) -> tuple:
        """
        Gets the default and custom data dictionaries for the selected table.

        :param remove_instance_data: Flag to remove instance data fields.
        :return: A tuple of default and custom data dictionaries.
        """
        # Get current table from both default and custom.
        default_table = self.get_defaults_table(self.type_selection)
        custom_table = self.get_custom_table(self.type_selection)

        # Get results for current selected unit name.
        default = self.model.query_first(default_table, Name=self.name)
        custom = self.model.query_first(custom_table, Name=self.name)

        if remove_instance_data:
            # Remove non-important fields from dict before comparison.
            default.__dict__.pop("_sa_instance_state")
            custom.__dict__.pop("_sa_instance_state")

        return default, custom

    def set_defaults(self) -> None:
        """
        Resets the view and custom model back to defaults.
        """
        names = self.check_custom_vs_defaults()
        try:
            default, custom = self.get_current_data()
            for name in names:
                custom.__setattr__(name, default.__getattribute__(name))

            # Persist the defaults to the custom database.
            self.model.update(custom)
            self.populate_data()
            self.update_model()
        except Exception as err:
            logger.error(f"{err}")

    def check_custom_vs_defaults(self) -> list:
        """
        Checks the custom vs the default dictionary to see if they are different.

        :return: The names of the items that are different.
        """
        default, custom = self.get_current_data(remove_instance_data=True)

        names = []

        # XOR operation to keep only elements that are different.
        unmatched_item = set(default.__dict__.items()) ^ set(custom.__dict__.items())

        # If there is a difference.
        if len(unmatched_item):
            # Get the name of the feature that is different.
            for item in unmatched_item:
                names.append(item[0])

        return list(set(names))

    @non_none_return_value
    def get_custom_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        key = key.lower()
        return {
            "aircraft": AircraftCustom,
            "buildings": BuildingsCustom,
            "infantry": InfantryCustom,
            "ships": ShipsCustom,
            "vehicles": VehiclesCustom
        }.get(key, None)

    @non_none_return_value
    def get_defaults_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        key = key.lower()
        return {
            "aircraft": AircraftDefault,
            "buildings": BuildingsDefault,
            "infantry": InfantryDefault,
            "ships": ShipsDefault,
            "vehicles": VehiclesDefault
        }.get(key, None)

    def populate_data(self, result: None = None) -> None:
        """
        Populates the data into the view from the model.

        :param result: The result to fill the model with data with.
        """
        selected_unit = self.view.unitComboBox.currentText()
        exclusion_list = ["name"]

        if len(selected_unit.strip()) != 0:

            # Get the first result of the given query. Should only equal one as Name is a unique field.
            result: UnitStructureType = self.model.query_first(self.table, Name=selected_unit)
            super().populate_data(result)

            # Assign the model data to the view.
            for prop_name in self.table.property_names().values():
                try:
                    self.__setattr__(prop_name, result)
                except AttributeError as err:

                    # If the prop_name isn't part of the know exclusion list, throw an error.
                    if prop_name not in exclusion_list:
                        logger.error(f"{err}")
                        raise err

            # Highlight fields that are different to the default.
            self.show_difference_highlighting()

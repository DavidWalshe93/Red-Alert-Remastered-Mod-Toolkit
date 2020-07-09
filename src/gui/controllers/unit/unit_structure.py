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


class UnitStructureController(VehiclesController, InfantryController, BuildingsController):

    def __init__(self, *args, **kwargs):
        """
        Controls updates to the GUI elements via the database.
        """
        super().__init__(*args, **kwargs)
        self.table = None

        self.bind_controller_slots()

        self.populate_units_based_on_type()
        self.populate_data()

    def bind_controller_slots(self) -> None:
        """
        Method to bind GUI actions to method callbacks.
        """
        self.view.unitTypeComboBox.currentTextChanged.connect(self.populate_units_based_on_type)
        self.view.unitComboBox.currentTextChanged.connect(self.populate_data)
        self.view.c4checkBox.stateChanged.connect(self.view.c4_adjust_dependencies)

        # self.view.ammoSpinBox.valueChanged.connect(self.update_db_on_change)

    def populate_units_based_on_type(self) -> None:
        """
        Populates the units field in the GUI.
        """
        # Get the table selected.
        key = self.table_selection
        self.table = self.get_custom_table(key)

        # Update the combobox with the fields associated with the table selected.
        items = self.model.all_ordered_by(self.table, self.table.Name)
        self.view.unitComboBox.clear()
        for i in items:
            self.view.unitComboBox.addItem(i.Name)

        # Update the view options based on the current state.
        self.view.update_options(key)

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
            # self.show_difference_highlighting()

    # def get_label_names(self) -> dict:
    #     """
    #     Gets a list of property names matching the table fields. Removes non GUI related fields.
    #
    #     :return: A dict of property label names.
    #     """
    #     label_names = super().get_label_names()
    #
    #     # Adjust naming for some fields.
    #     label_names.update({"rot": label_names.pop("ROT")})
    #
    #     return label_names

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

    def get_default_table(self, key):
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

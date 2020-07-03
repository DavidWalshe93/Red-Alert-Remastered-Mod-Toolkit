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


from src.db_driver.models.units.buildings import Buildings, BuildingsDefault, BuildingsCustom
from src.db_driver.models.units.aircraft import Aircraft, AircraftDefault, AircraftCustom
from src.db_driver.models.units.infantry import Infantry, InfantryDefault, InfantryCustom
from src.db_driver.models.units.ships import Ships, ShipsDefault, ShipsCustom
from src.db_driver.models.units.vehicles import Vehicles, VehiclesDefault, VehiclesCustom

from src.gui.controllers.utils import set_checked, is_checked

UnitStructureType = Union[Aircraft, Infantry, Vehicles, Buildings, Ships]

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


class UnitCoreController(VehiclesController, InfantryController, BuildingsController):

    def __init__(self, *args, **kwargs):
        """
        Controls updates to the GUI elements via the database.
        """
        super().__init__(*args, **kwargs)
        self.table = None
        self.populate_units_based_on_type()
        self.populate_data()

        self.shortcut_open = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+S'), self.view)

    def bind_slots(self):
        self.view.unitTypeComboBox.currentTextChanged.connect(self.populate_units_based_on_type)
        self.view.unitComboBox.currentTextChanged.connect(self.populate_data)
        self.view.c4checkBox.stateChanged.connect(self.c4_disable_dependencies)
        self.view.saveButton.clicked.connect(self.update_model)
        self.view.defaultsButton.clicked.connect(self.set_defaults)

        self.shortcut_open.activated.connect(self.update_model)

    def populate_units_based_on_type(self):
        key = self.type_selection
        self.table = self.get_custom_table(key)
        items = self.model.all_ordered_by(self.table, self.table.Name)
        self.view.unitComboBox.clear()
        for i in items:
            self.view.unitComboBox.addItem(i.Name)

        self.update_change_highlight()

        self.view.update_options(key)

    def update_model(self):
        try:
            item = self.model.query_first(self.table, Name=self.name)
            name_mapping: dict = self.table.property_names()
            for column_name, property_name in name_mapping.items():
                if column_name not in ["Id", "Tag"]:
                    try:
                        item.__setattr__(column_name, self.__getattribute__(property_name))
                    except Exception as err:
                        raise err
            self.model.update(item)
            logger.info(f"Successfully updated {name_mapping['Name']} with ")
            self.update_change_highlight()
        except Exception as err:
            logger.error(f"Could not update model - {err}")

    def set_defaults(self):
        names = self.check_custom_vs_defaults()
        try:
            default, custom = self.get_current_data()
            for name in names:
                custom.__setattr__(name, default.__getattribute__(name))
            self.model.update(custom)
            self.populate_data()
            self.update_model()
        except Exception as err:
            logger.error(f"{err}")

    def get_current_data(self, remove_instance_data: bool = False) -> tuple:
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

    def check_custom_vs_defaults(self) -> list:

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

    def update_change_highlight(self):
        names = self.check_custom_vs_defaults()
        label_names: dict = self.table.property_names()
        label_names.pop("Id")
        label_names.pop("Name")
        label_names.pop("Tag")

        label_names.update({"rot": label_names.pop("ROT")})
        for label in label_names.keys():
            object_name = f"{label[0].lower()}{label[1:]}Label"

            if label in names:
                self.view.__getattribute__(f"{object_name}").setStyleSheet("QLabel { background-color : black; color : white; font-size: 12px; }")
            else:
                self.view.__getattribute__(f"{object_name}").setStyleSheet("QLabel {  background-color : white; color : black; font-size: 12px; }")

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

    def c4_disable_dependencies(self):
        if self.c4 == "yes":
            self.view.infiltrateCheckBox.setEnabled(False)
        else:
            self.view.infiltrateCheckBox.setEnabled(True)

    def populate_data(self, result: None = None):
        if len(self.view.unitComboBox.currentText().strip()) != 0:
            result: UnitStructureType = self.model.query(self.table, Name=self.view.unitComboBox.currentText())[0]
            super().populate_data(result)
            for prop_name in self.table.property_names().values():
                try:
                    self.__setattr__(prop_name, result)
                except AttributeError as err:
                    if prop_name not in ["name"]:
                        raise err

    @property
    def type_selection(self):
        return self.view.unitTypeComboBox.currentText()

    @property
    def name(self):
        return self.view.unitComboBox.currentText()

    @property
    def ammo(self):
        return self.view.ammoSpinBox.value()

    @ammo.setter
    def ammo(self, value: UnitStructureType):
        self.view.ammoSpinBox.setValue(value.Ammo)

    @property
    def armor(self):
        return self.view.armorComboBox.currentText()

    @armor.setter
    def armor(self, value: UnitStructureType):
        self.view.armorComboBox.setCurrentText(value.Armor)

    @property
    def cloakable(self):
        return is_checked(self.view.cloakableCheckBox)

    @cloakable.setter
    def cloakable(self, value: UnitStructureType):
        self.view.cloakableCheckBox.setCheckState(set_checked(value.Cloakable))

    @property
    def cost(self):
        return self.view.costSpinBox.value()

    @cost.setter
    def cost(self, value: UnitStructureType):
        self.view.costSpinBox.setValue(value.Cost)

    @property
    def double_owned(self):
        return is_checked(self.view.doubleOwnedCheckBox)

    @double_owned.setter
    def double_owned(self, value: UnitStructureType):
        self.view.doubleOwnedCheckBox.setCheckState(set_checked(value.DoubleOwned))

    @property
    def explodes(self):
        return is_checked(self.view.explodesCheckBox)

    @explodes.setter
    def explodes(self, value: UnitStructureType):
        self.view.explodesCheckBox.setCheckState(set_checked(value.Explodes))

    @property
    def guard_range(self):
        return None if self.view.guardRangeSpinBox.value() == -1 else self.view.guardRangeSpinBox.value()

    @guard_range.setter
    def guard_range(self, value: UnitStructureType):
        value = value.GuardRange if value.GuardRange is not None else -1
        self.view.guardRangeSpinBox.setValue(value)

    @property
    def image(self):
        data = self.view.imageComboBox.currentText()
        return data if data != "" else None

    @image.setter
    def image(self, value: UnitStructureType):
        self.view.imageComboBox.setCurrentText(value.Image)

    @property
    def invisible(self):
        return is_checked(self.view.invisibleCheckBox)

    @invisible.setter
    def invisible(self, value: UnitStructureType):
        self.view.invisibleCheckBox.setCheckState(set_checked(value.Invisible))

    @property
    def owner(self):
        return self.view.ownerComboBox.currentText()

    @owner.setter
    def owner(self, value: UnitStructureType):
        self.view.ownerComboBox.setCurrentText(value.Owner)

    @property
    def points(self):
        return self.view.pointsSpinBox.value()

    @points.setter
    def points(self, value: UnitStructureType):
        self.view.pointsSpinBox.setValue(value.Points)

    @property
    def prerequisite(self):
        return self.view.prerequisiteLineEdit.text()

    @prerequisite.setter
    def prerequisite(self, value: UnitStructureType):
        self.view.prerequisiteLineEdit.setText(value.Prerequisite)

    @property
    def primary(self):
        return self.view.primaryComboBox.currentText()

    @primary.setter
    def primary(self, value: UnitStructureType):
        self.view.primaryComboBox.setCurrentText(value.Primary)

    @property
    def secondary(self):
        return self.view.secondaryComboBox.currentText()

    @secondary.setter
    def secondary(self, value: UnitStructureType):
        self.view.secondaryComboBox.setCurrentText(value.Secondary)

    @property
    def rot(self):
        return self.view.rotSpinBox.value()

    @rot.setter
    def rot(self, value: UnitStructureType):
        self.view.rotSpinBox.setValue(value.ROT)

    @property
    def reload(self):
        return self.view.reloadSpinBox.value()

    @reload.setter
    def reload(self, value: UnitStructureType):
        self.view.reloadSpinBox.setValue(value.Reload)

    @property
    def self_healing(self):
        return is_checked(self.view.selfHealingCheckBox)

    @self_healing.setter
    def self_healing(self, value: UnitStructureType):
        self.view.selfHealingCheckBox.setCheckState(set_checked(value.SelfHealing))

    @property
    def sight(self):
        return self.view.sightSpinBox.value()

    @sight.setter
    def sight(self, value: UnitStructureType):
        self.view.sightSpinBox.setValue(value.Sight)

    @property
    def strength(self):
        return self.view.healthSpinBox.value()

    @strength.setter
    def strength(self, value: UnitStructureType):
        self.view.healthSpinBox.setValue(value.Strength)

    @property
    def sensors(self):
        return is_checked(self.view.sensorsCheckBox)

    @sensors.setter
    def sensors(self, value: UnitStructureType):
        self.view.sensorsCheckBox.setCheckState(set_checked(value.Sensors))

    @property
    def tech_level(self):
        return self.view.techLevelSpinBox.value()

    @tech_level.setter
    def tech_level(self, value: UnitStructureType):
        self.view.techLevelSpinBox.setValue(value.TechLevel)

"""
Author:     David Walshe
Date:       29 June 2020
"""

import functools
import logging
from typing import Union

from src.gui.controllers.contoller import Controller
from src.db_driver.table_drivers.units import Aircraft, Infantry, Vehicles, Ships, Buildings

UnitType = Union[Aircraft, Infantry, Vehicles, Buildings, Ships]

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


class UnitController(Controller):

    def __init__(self, *args, **kwargs):
        """
        Controls updates to the GUI elements via the database.
        """
        super().__init__(*args, **kwargs)
        self.table_cls = None
        self.populate_units_based_on_type()
        self.populate_data_based_on_unit()

    def bind_slots(self):
        self.view.unitTypeComboBox.currentTextChanged.connect(self.populate_units_based_on_type)
        self.view.unitComboBox.currentTextChanged.connect(self.populate_data_based_on_unit)

    def populate_units_based_on_type(self):
        key = self.view.unitTypeComboBox.currentText()
        self.table_cls = self.get_table(key)
        items = self.db.all_ordered_by(self.table_cls, self.table_cls.Name)
        self.view.unitComboBox.clear()
        for i in items:
            self.view.unitComboBox.addItem(i.Name)

    def populate_data_based_on_unit(self):
        if len(self.view.unitComboBox.currentText().strip()) != 0:
            try:
                result: UnitType = self.db.query(self.table_cls, Name=self.view.unitComboBox.currentText())[0]
                self.ammo = result
                self.armor = result
                self.cloakable = result
                self.cost = result
                self.doubleOwned = result
                self.guard_range = result
                self.image = result
                self.invisible = result
                self.owner = result
                self.points = result
                self.prerequisite = result
                self.primary = result
                self.secondary = result
                self.rot = result
                self.reload = result
                self.self_healing = result
                self.sight = result
                self.strength = result
                self.tech_level = result
                self.sensors = result

            except Exception as err:
                logger.error(f"{err}")
                raise err

    @property
    def ammo(self):
        return self.view.ammoSpinBox.value()

    @ammo.setter
    def ammo(self, value: UnitType):
        self.view.ammoSpinBox.setValue(value.Ammo)

    @property
    def armor(self):
        return self.view.armorComboBox.currentText()

    @armor.setter
    def armor(self, value: UnitType):
        self.view.armorComboBox.setCurrentText(value.Armor)

    @property
    def cloakable(self):
        return self.view.cloakableComboBox.currentText()

    @cloakable.setter
    def cloakable(self, value: UnitType):
        self.view.cloakableComboBox.setCurrentText(value.Cloakable)

    @property
    def cost(self):
        return self.view.costSpinBox.value()

    @cost.setter
    def cost(self, value: UnitType):
        self.view.costSpinBox.setValue(value.Cost)

    @property
    def doubleOwned(self):
        return self.view.doubleOwnedComboBox.currentText()

    @doubleOwned.setter
    def doubleOwned(self, value: UnitType):
        self.view.doubleOwnedComboBox.setCurrentText(value.DoubleOwned)

    @property
    def explodes(self):
        return self.view.explodesComboBox.currentText()

    @explodes.setter
    def explodes(self, value: UnitType):
        self.view.explodesComboBox.setView(value.Explodes)

    @property
    def guard_range(self):
        return None if self.view.guardRangeSpinBox.value() == -1 else self.view.guardRangeSpinBox.value()

    @guard_range.setter
    def guard_range(self, value: UnitType):
        value = value.GuardRange if value.GuardRange is not None else -1
        self.view.guardRangeSpinBox.setValue(value)

    @property
    def image(self):
        return self.view.imageComboBox.currentText()

    @image.setter
    def image(self, value: UnitType):
        self.view.imageComboBox.setCurrentText(value.Image)

    @property
    def invisible(self):
        return self.view.invisibleComboBox.currentText()

    @invisible.setter
    def invisible(self, value: UnitType):
        self.view.invisibleComboBox.setCurrentText(value.Invisible)

    @property
    def owner(self):
        return self.view.ownerComboBox.currentText()

    @owner.setter
    def owner(self, value: UnitType):
        self.view.ownerComboBox.setCurrentText(value.Owner)

    @property
    def points(self):
        return self.view.pointsSpinBox.value()

    @points.setter
    def points(self, value: UnitType):
        self.view.pointsSpinBox.setValue(value.Points)

    @property
    def prerequisite(self):
        return self.view.prerequisiteLineEdit.text()

    @prerequisite.setter
    def prerequisite(self, value: UnitType):
        self.view.prerequisiteLineEdit.setText(value.Prerequisite)

    @property
    def primary(self):
        return self.view.primaryComboBox.currentText()

    @primary.setter
    def primary(self, value: UnitType):
        self.view.primaryComboBox.setCurrentText(value.Primary)

    @property
    def secondary(self):
        return self.view.secondaryComboBox.currentText()

    @secondary.setter
    def secondary(self, value: UnitType):
        self.view.secondaryComboBox.setCurrentText(value.Secondary)

    @property
    def rot(self):
        return self.view.primaryComboBox.currentText()

    @rot.setter
    def rot(self, value: UnitType):
        self.view.rotSpinBox.setValue(value.ROT)

    @property
    def reload(self):
        return self.view.reloadSpinBox.value()

    @reload.setter
    def reload(self, value: UnitType):
        self.view.reloadSpinBox.setValue(value.Reload)

    @property
    def self_healing(self):
        return self.view.selfHealingComboBox.currentText()

    @self_healing.setter
    def self_healing(self, value: UnitType):
        self.view.selfHealingComboBox.setCurrentText(value.SelfHealing)

    @property
    def sight(self):
        return self.view.sightSpinBox.value()

    @sight.setter
    def sight(self, value: UnitType):
        self.view.sightSpinBox.setValue(value.Sight)

    @property
    def strength(self):
        return self.view.healthSpinBox.currentText()

    @strength.setter
    def strength(self, value: UnitType):
        self.view.healthSpinBox.setValue(value.Strength)

    @property
    def tech_level(self):
        return self.view.techLevelSpinBox.value()

    @tech_level.setter
    def tech_level(self, value: UnitType):
        self.view.techLevelSpinBox.setValue(value.TechLevel)

    @property
    def sensors(self):
        return self.view.sensorsComboBox.currentText()

    @sensors.setter
    def sensors(self, value: UnitType):
        self.view.sensorsComboBox.setCurrentText(value.Sensors.lower())

    @non_none_return_value
    def get_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        key = key.lower()
        logger.info(f"Key value passed to get_table() = {key}")
        return {
            "aircraft": Aircraft,
            "buildings": Buildings,
            "infantry": Infantry,
            "ships": Ships,
            "vehicles": Vehicles
        }.get(key, None)

"""
Author:     David Walshe
Date:       05 July 2020
"""

from abc import ABC
from typing import Union

from src.gui.controllers.utils import set_checked, is_checked
from src.gui.controllers.contoller import Controller
from src.db_driver.models.units.vehicles import Vehicles
from src.db_driver.models.units.aircraft import Aircraft
from src.db_driver.models.units.ships import Ships
from src.db_driver.models.units.infantry import Infantry
from src.db_driver.models.units.buildings import Buildings

UnitType = Union[Aircraft, Infantry, Ships, Vehicles]
UnitStructureType = Union[Aircraft, Infantry, Vehicles, Buildings, Ships]


class CoreController(Controller, ABC):

    def populate_data(self, result: any):
        super().populate_data(result)

    @staticmethod
    def is_unit(obj) -> bool:
        """
        Checks if the object passed is an instance of a Unit class.

        :param obj: The object to check.
        :return: True if it is an instance of a Unit class, False otherwise
        """
        return isinstance(obj, (Aircraft, Infantry, Ships, Vehicles))

    @staticmethod
    def is_building(obj) -> bool:
        """
        Checks if the object passed is an instance of a Building class.

        :param obj: The object to check.
        :return: True if it is an instance of a Building class, False otherwise
        """
        return isinstance(obj, Buildings)

    @property
    def table_selection(self):
        return self.view.unitTypeComboBox.currentText()

    @table_selection.setter
    def table_selection(self, value):
        pass

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

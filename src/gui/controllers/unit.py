"""
Author:     David Walshe
Date:       29 June 2020
"""

import functools
import logging
from typing import Union

from PyQt5 import QtWidgets, QtCore

from src.gui.controllers.contoller import Controller
from src.db_driver.models.units import Aircraft, Infantry, Vehicles, Ships, Buildings

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
        self.view.ammoLabel.setStyleSheet("QLabel { background-color : red; color : blue; }")

    def bind_slots(self):
        self.view.unitTypeComboBox.currentTextChanged.connect(self.populate_units_based_on_type)
        self.view.unitComboBox.currentTextChanged.connect(self.populate_data_based_on_unit)
        self.view.c4checkBox.stateChanged.connect(self.c4_disable_dependencies)

    def populate_units_based_on_type(self):
        key = self.view.unitTypeComboBox.currentText()
        self.table_cls = self.get_table(key)
        items = self.db.all_ordered_by(self.table_cls, self.table_cls.Name)
        self.view.unitComboBox.clear()
        for i in items:
            self.view.unitComboBox.addItem(i.Name)

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

    def c4_disable_dependencies(self):
        if self.c4 == "yes":
            self.view.infiltrateCheckBox.setEnabled(False)
        else:
            self.view.infiltrateCheckBox.setEnabled(True)

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
                if type(result) is Buildings:
                    self.base_normal = result
                    self.adjacent = result
                    self.bib = result
                    self.capturable = result
                    self.crewed = result
                    self.power = result
                    self.powered = result
                    self.repairable = result
                    self.storage = result
                    self.unsellable = result
                    self.water_bound = result
                    pass
                else:
                    self.passengers = result
                    self.speed = result
                    if type(result) is Infantry:
                        self.c4 = result
                        self.fraidycat = result
                        self.infiltrate = result
                        self.is_canine = result
                    elif type(result) is Vehicles:
                        self.crushable = result
                        self.tracked = result
                        self.no_moving_fire = result

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
        return self.is_checked(self.view.cloakableCheckBox)

    @cloakable.setter
    def cloakable(self, value: UnitType):
        self.view.cloakableCheckBox.setCheckState(self.set_checked(value.Cloakable))

    @property
    def cost(self):
        return self.view.costSpinBox.value()

    @cost.setter
    def cost(self, value: UnitType):
        self.view.costSpinBox.setValue(value.Cost)

    @property
    def doubleOwned(self):
        return self.is_checked(self.view.doubleOwnedCheckBox)

    @doubleOwned.setter
    def doubleOwned(self, value: UnitType):
        self.view.doubleOwnedCheckBox.setCheckState(self.set_checked(value.DoubleOwned))

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
        return self.is_checked(self.view.invisibleCheckBox)

    @invisible.setter
    def invisible(self, value: UnitType):
        self.view.invisibleCheckBox.setCheckState(self.set_checked(value.Invisible))

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
        return self.is_checked(self.view.selfHealingLabel)

    @self_healing.setter
    def self_healing(self, value: UnitType):
        self.view.selfHealingCheckBox.setCheckState(self.set_checked(value.SelfHealing))

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
    def sensors(self):
        return self.is_checked(self.view.sensorsCheckBox)

    @sensors.setter
    def sensors(self, value: UnitType):
        self.view.sensorsCheckBox.setCheckState(self.set_checked(value.Sensors))

    @property
    def tech_level(self):
        return self.view.techLevelSpinBox.value()

    @tech_level.setter
    def tech_level(self, value: UnitType):
        self.view.techLevelSpinBox.setValue(value.TechLevel)

    @property
    def passengers(self):
        return self.view.passengersSpinBox.value()

    @passengers.setter
    def passengers(self, value: UnitType):
        self.view.passengersSpinBox.setValue(value.Passengers)

    @property
    def speed(self):
        return self.view.speedSpinBox.value()

    @speed.setter
    def speed(self, value: UnitType):
        self.view.speedSpinBox.setValue(value.Speed)

    @property
    def c4(self):
        return self.is_checked(self.view.c4checkBox)

    @c4.setter
    def c4(self, value: UnitType):
        self.view.c4checkBox.setCheckState(self.set_checked(value.C4))

    @property
    def fraidycat(self):
        return self.is_checked(self.view.fraidycatCheckBox)

    @fraidycat.setter
    def fraidycat(self, value: UnitType):
        self.view.fraidycatCheckBox.setCheckState(self.set_checked(value.Fraidycat))

    @property
    def infiltrate(self):
        return self.is_checked(self.view.infiltrateCheckBox)

    @infiltrate.setter
    def infiltrate(self, value: UnitType):
        self.view.infiltrateCheckBox.setCheckState(self.set_checked(value.Infiltrate))

    @property
    def is_canine(self):
        return self.is_checked(self.view.isCanineCheckBox)

    @is_canine.setter
    def is_canine(self, value: UnitType):
        self.view.isCanineCheckBox.setCheckState(self.set_checked(value.IsCanine))

    @property
    def crushable(self):
        return self.is_checked(self.view.crushableCheckBox)

    @crushable.setter
    def crushable(self, value: UnitType):
        self.view.crushableCheckBox.setCheckState(self.set_checked(value.Crushable))

    @property
    def tracked(self):
        return self.is_checked(self.view.trackedCheckBox)

    @tracked.setter
    def tracked(self, value: UnitType):
        self.view.trackedCheckBox.setCheckState(self.set_checked(value.Tracked))

    @property
    def no_moving_fire(self):
        return self.is_checked(self.view.noMovingFireCheckBox)

    @no_moving_fire.setter
    def no_moving_fire(self, value: UnitType):
        self.view.noMovingFireCheckBox.setCheckState(self.set_checked(value.NoMovingFire))

    @property
    def base_normal(self):
        return self.is_checked(self.view.baseNormalCheckBox)
    
    @base_normal.setter
    def base_normal(self, value: UnitType):
        self.view.baseNormalCheckBox.setCheckState(self.set_checked(value.BaseNormal))
    
    @property
    def adjacent(self):
        return self.view.adjacentSpinBox.value()
    
    @adjacent.setter
    def adjacent(self, value: UnitType):
        self.view.adjacentSpinBox.setValue(value.Adjacent)
        
    @property
    def bib(self):
        return self.is_checked(self.view.bibCheckBox)
    
    @bib.setter
    def bib(self, value: UnitType):
        self.view.bibCheckBox.setCheckState(self.set_checked(value.Bib))
        
    @property
    def capturable(self):
        return self.is_checked(self.view.capturableCheckBox)
    
    @capturable.setter
    def capturable(self, value: UnitType):
        self.view.capturableCheckBox.setCheckState(self.set_checked(value.Capturable))
        
    @property
    def crewed(self):
        return self.is_checked(self.view.crewedCheckBox)
    
    @crewed.setter
    def crewed(self, value: UnitType):
        self.view.crewedCheckBox.setCheckState(self.set_checked(value.Crewed))

    @property
    def power(self):
        return self.view.powerSpinBox.value()

    @power.setter
    def power(self, value: UnitType):
        self.view.powerSpinBox.setValue(value.Power)

    @property
    def powered(self):
        return self.is_checked(self.view.poweredCheckBox)

    @powered.setter
    def powered(self, value: UnitType):
        self.view.poweredCheckBox.setCheckState(self.set_checked(value.Powered))

    @property
    def repairable(self):
        return self.is_checked(self.view.repairableCheckBox)

    @repairable.setter
    def repairable(self, value: UnitType):
        self.view.repairableCheckBox.setCheckState(self.set_checked(value.Repairable))

    @property
    def storage(self):
        return self.view.storageSpinBox.value()
    
    @storage.setter
    def storage(self, value: UnitType):
        self.view.storageSpinBox.setValue(value.Storage)

    @property
    def unsellable(self):
        return self.is_checked(self.view.unsellableCheckBox)

    @unsellable.setter
    def unsellable(self, value: UnitType):
        self.view.unsellableCheckBox.setCheckState(self.set_checked(value.Unsellable))
        
    @property
    def water_bound(self):
        return self.is_checked(self.view.waterBoundCheckBox)
    
    @water_bound.setter
    def water_bound(self, value: UnitType):
        self.view.waterBoundCheckBox.setCheckState(self.set_checked(value.WaterBound))
    
    @staticmethod
    def is_checked(checkbox: QtWidgets.QCheckBox):
        return "yes" if checkbox.isChecked() else "no"

    @staticmethod
    def set_checked(value) -> bool:
        return True if value.lower() == "yes" else False

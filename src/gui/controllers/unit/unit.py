"""
Author:     David Walshe
Date:       03 July 2020
"""
from abc import ABC

from src.gui.controllers.utils import set_checked, is_checked
from src.gui.controllers.contoller import Controller
from src.db_driver.models.units.vehicles import Vehicles
from src.db_driver.models.units.aircraft import Aircraft
from src.db_driver.models.units.ships import Ships
from src.db_driver.models.units.infantry import Infantry


from typing import Union

UnitType = Union[Aircraft, Infantry, Ships, Vehicles]


class UnitController(Controller, ABC):

    def populate_data(self, result: UnitType):
        super().populate_data(result)
        if isinstance(result, (Aircraft, Infantry, Ships, Vehicles)):
            self.passengers = result
            self.speed = result

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
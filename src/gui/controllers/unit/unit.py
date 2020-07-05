"""
Author:     David Walshe
Date:       03 July 2020
"""

from abc import ABC

from src.gui.controllers.utils import set_checked, is_checked
from src.gui.controllers.unit.core import CoreController, UnitType


class UnitController(CoreController, ABC):

    def populate_data(self, result: UnitType) -> None:
        """
        Populates the data from the database into the view.

        :param result: The database query result.
        """
        super().populate_data(result)
        if self.is_unit(result):
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

"""
Author:     David Walshe
Date:       03 July 2020
"""
from abc import ABC

from src.gui.controllers.utils import set_checked, is_checked
from src.gui.controllers.unit.unit import UnitController
from src.db_driver.models.units.vehicles import Vehicles


class VehiclesController(UnitController, ABC):

    def populate_data(self, result: Vehicles):
        super().populate_data(result)
        if isinstance(result, Vehicles):
            self.crushable = result
            self.tracked = result
            self.no_moving_fire = result

    @property
    def crushable(self):
        return is_checked(self.view.crushableCheckBox)

    @crushable.setter
    def crushable(self, value: Vehicles):
        self.view.crushableCheckBox.setCheckState(set_checked(value.Crushable))

    @property
    def tracked(self):
        return is_checked(self.view.trackedCheckBox)

    @tracked.setter
    def tracked(self, value: Vehicles):
        self.view.trackedCheckBox.setCheckState(set_checked(value.Tracked))

    @property
    def no_moving_fire(self):
        return is_checked(self.view.noMovingFireCheckBox)

    @no_moving_fire.setter
    def no_moving_fire(self, value: Vehicles):
        self.view.noMovingFireCheckBox.setCheckState(set_checked(value.NoMovingFire))

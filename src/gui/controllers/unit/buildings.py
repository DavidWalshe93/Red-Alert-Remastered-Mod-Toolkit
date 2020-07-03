"""
Author:     David Walshe
Date:       03 July 2020
"""
from abc import ABC

from src.gui.controllers.utils import set_checked, is_checked
from src.gui.controllers.contoller import Controller
from src.db_driver.models.units.buildings import Buildings


class BuildingsController(Controller, ABC):

    def populate_data(self, result: Buildings):
        super().populate_data(result)
        if isinstance(result, Buildings):
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

    @property
    def base_normal(self):
        return is_checked(self.view.baseNormalCheckBox)

    @base_normal.setter
    def base_normal(self, value: Buildings):
        self.view.baseNormalCheckBox.setCheckState(set_checked(value.BaseNormal))

    @property
    def adjacent(self):
        return self.view.adjacentSpinBox.value()

    @adjacent.setter
    def adjacent(self, value: Buildings):
        self.view.adjacentSpinBox.setValue(value.Adjacent)

    @property
    def bib(self):
        return is_checked(self.view.bibCheckBox)

    @bib.setter
    def bib(self, value: Buildings):
        self.view.bibCheckBox.setCheckState(set_checked(value.Bib))

    @property
    def capturable(self):
        return is_checked(self.view.capturableCheckBox)

    @capturable.setter
    def capturable(self, value: Buildings):
        self.view.capturableCheckBox.setCheckState(set_checked(value.Capturable))

    @property
    def crewed(self):
        return is_checked(self.view.crewedCheckBox)

    @crewed.setter
    def crewed(self, value: Buildings):
        self.view.crewedCheckBox.setCheckState(set_checked(value.Crewed))

    @property
    def power(self):
        return self.view.powerSpinBox.value()

    @power.setter
    def power(self, value: Buildings):
        self.view.powerSpinBox.setValue(value.Power)

    @property
    def powered(self):
        return is_checked(self.view.poweredCheckBox)

    @powered.setter
    def powered(self, value: Buildings):
        self.view.poweredCheckBox.setCheckState(set_checked(value.Powered))

    @property
    def repairable(self):
        return is_checked(self.view.repairableCheckBox)

    @repairable.setter
    def repairable(self, value: Buildings):
        self.view.repairableCheckBox.setCheckState(set_checked(value.Repairable))

    @property
    def storage(self):
        return self.view.storageSpinBox.value()

    @storage.setter
    def storage(self, value: Buildings):
        self.view.storageSpinBox.setValue(value.Storage)

    @property
    def unsellable(self):
        return is_checked(self.view.unsellableCheckBox)

    @unsellable.setter
    def unsellable(self, value: Buildings):
        self.view.unsellableCheckBox.setCheckState(set_checked(value.Unsellable))

    @property
    def water_bound(self):
        return is_checked(self.view.waterBoundCheckBox)

    @water_bound.setter
    def water_bound(self, value: Buildings):
        self.view.waterBoundCheckBox.setCheckState(set_checked(value.WaterBound))
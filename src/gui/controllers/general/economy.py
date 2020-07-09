"""
Author:     David Walshe
Date:       06 July 2020
"""

from abc import ABC, abstractmethod
from src.gui.controllers.general.core import CoreController
from src.db_driver.models.general import General
from src.gui.controllers.utils import set_checked, is_checked


class EconomyController(CoreController, ABC):

    @property
    def bail_count(self):
        return self.view.bailCountSpinBox.value()

    @bail_count.setter
    def bail_count(self, value: General):
        self.view.bailCountSpinBox.setValue(value.BailCount)

    @property
    def build_speed(self):
        return self.view.buildSpeedSpinBox.value()

    @build_speed.setter
    def build_speed(self, value: General):
        self.view.buildSpeedSpinBox.setValue(value.BuildSpeed)

    @property
    def gem_value(self):
        return self.view.gemValueSpinBox.value()

    @gem_value.setter
    def gem_value(self, value: General):
        self.view.gemValueSpinBox.setValue(value.GemValue)

    @property
    def gold_value(self):
        return self.view.goldValueSpinBox.value()

    @gold_value.setter
    def gold_value(self, value: General):
        self.view.goldValueSpinBox.setValue(value.GoldValue)

    @property
    def growth_rate(self):
        return self.view.growthRateSpinBox.value()

    @growth_rate.setter
    def growth_rate(self, value: General):
        self.view.growthRateSpinBox.setValue(value.GrowthRate)

    @property
    def ore_grows(self):
        return is_checked(self.view.oreGrowsCheckBox)

    @ore_grows.setter
    def ore_grows(self, value: General):
        self.view.oreGrowsCheckBox.setCheckState(set_checked(value.OreGrows))

    @property
    def ore_spreads(self):
        return is_checked(self.view.oreSpreadsCheckBox)

    @ore_spreads.setter
    def ore_spreads(self, value: General):
        self.view.oreSpreadsCheckBox.setCheckState(set_checked(value.OreSpreads))

    @property
    def ore_truck_rate(self):
        return self.view.oreTruckRateSpinBox.value()

    @ore_truck_rate.setter
    def ore_truck_rate(self, value: General):
        self.view.oreTruckRateSpinBox.setValue(value.OreTruckRate)

    @property
    def separate_aircraft(self):
        return is_checked(self.view.separateAircraftCheckBox)

    @separate_aircraft.setter
    def separate_aircraft(self, value: General):
        self.view.separateAircraftCheckBox.setCheckState(set_checked(value.SeparateAircraft))

    @property
    def survivor_rate(self):
        return self.view.survivorRateSpinBox.value()

    @survivor_rate.setter
    def survivor_rate(self, value: General):
        self.view.survivorRateSpinBox.setValue(value.SurvivorRate)

"""
Author:     David Walshe
Date:       06 July 2020
"""

from src.gui.controllers.general.economy import EconomyController
from src.gui.controllers.general.combat import CombatController
from src.db_driver.models.general import GeneralDefaults, GeneralCustom


class GeneralController(EconomyController, CombatController):

    def __init__(self, *args, **kwargs):
        """
        Controls updates to the GUI elements via the database.
        """
        super().__init__(*args, *kwargs)

        self.populate_data()

    def populate_data(self, result=None) -> None:
        table = GeneralCustom

        # There is only one record in this table.
        result = self.model.query_first(table)
        self.bail_count = result
        self.build_speed = result
        self.gem_value = result
        self.gold_value = result
        self.growth_rate = result
        self.ore_grows = result
        self.ore_spreads = result
        self.ore_truck_rate = result
        self.separate_aircraft = result
        self.survivor_rate = result

    @property
    def table(self):
        return self.get_custom_table()

    def get_custom_table(self, *args):
        return GeneralCustom

    def get_defaults_table(self, *args):
        return GeneralDefaults

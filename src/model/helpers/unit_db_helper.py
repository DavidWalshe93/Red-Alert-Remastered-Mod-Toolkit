"""
Author:     David Walshe
Date:       05 July 2020
"""

from src.model.helpers.core_db_helper import CoreDBHelper

from src.model.models.units.vehicles import VehiclesCustom, VehiclesDefault
from src.model.models.units.infantry import InfantryCustom, InfantryDefault
from src.model.models.units.buildings import BuildingsCustom, BuildingsDefault
from src.model.models.units.ships import ShipsCustom, ShipsDefault
from src.model.models.units.aircraft import AircraftCustom, AircraftDefault


class UnitDBHelper(CoreDBHelper):

    @property
    def buildings(self):
        return self.get_change_records(BuildingsDefault, BuildingsCustom)

    @property
    def infantry(self) -> list:
        return self.get_change_records(InfantryDefault, InfantryCustom)

    @property
    def aircraft(self):
        return self.get_change_records(AircraftDefault, AircraftCustom)

    @property
    def ships(self):
        return self.get_change_records(ShipsDefault, ShipsCustom)

    @property
    def vehicles(self):
        return self.get_change_records(VehiclesDefault, VehiclesCustom)
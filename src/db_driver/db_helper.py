"""
Author:     David Walshe
Date:       03 July 2020
"""

from src.db_driver.db_manager import DBManager

from src.db_driver.models.units.vehicles import VehiclesCustom, VehiclesDefault
from src.db_driver.models.units.infantry import InfantryCustom, InfantryDefault
from src.db_driver.models.units.buildings import BuildingsCustom, BuildingsDefault
from src.db_driver.models.units.ships import ShipsCustom, ShipsDefault
from src.db_driver.models.units.aircraft import AircraftCustom, AircraftDefault


class DBHelper(DBManager):

    @property
    def buildings(self):
        custom_records = self.all(BuildingsCustom)
        default_records = self.all(BuildingsDefault)

        for custom_record, default_record in zip(custom_records, default_records):
            default_record = default_record.__dict__
            custom_record = custom_record.__dict__

            default_record.__dict__.pop("_sa_instance_state")
            custom_record.__dict__.pop("_sa_instance_state")

            diff = set(default.items()) ^ set(custom.items())
            diff = [item[0] for item in diff]

            diff_dict = {key: custom_record[key] for key in diff}

            diff_dict.update({
                "Tag": custom_record["Tag"]
            })


        return self.all(BuildingsCustom)

    @property
    def infantry(self) -> list:
        custom_records = self.all(InfantryCustom)
        default_records = self.all(InfantryDefault)

        items = []
        for custom_record, default_record in zip(custom_records, default_records):
            default_record = default_record.__dict__
            custom_record = custom_record.__dict__

            default_record.pop("_sa_instance_state")
            custom_record.pop("_sa_instance_state")

            diff = set(default_record.items()) ^ set(custom_record.items())
            diff = [item[0] for item in diff]

            diff_dict = {key: custom_record[key] for key in diff}

            if len(diff_dict):
                diff_dict.update({
                    "Tag": custom_record["Tag"],
                    "Name": custom_record["Name"]
                })

                items.append(diff_dict)

        return items

    @property
    def aircraft(self):
        return self.all(AircraftCustom)

    @property
    def ships(self):
        return self.all(ShipsCustom)

    @property
    def vehicles(self):
        return self.all(VehiclesCustom)
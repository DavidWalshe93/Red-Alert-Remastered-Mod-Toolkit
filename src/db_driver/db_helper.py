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

    def __get_change_records(self, default_table, custom_table):
        default_records = self.all(default_table)
        custom_records = self.all(custom_table)

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

        print(items)

        return items

    @property
    def buildings(self):
        return self.__get_change_records(BuildingsDefault, BuildingsCustom)

    @property
    def infantry(self) -> list:
        return self.__get_change_records(InfantryDefault, InfantryCustom)

    @property
    def aircraft(self):
        return self.__get_change_records(AircraftDefault, AircraftCustom)

    @property
    def ships(self):
        return self.__get_change_records(ShipsDefault, ShipsCustom)

    @property
    def vehicles(self):
        return self.__get_change_records(VehiclesDefault, VehiclesCustom)
"""
Author:     David Walshe
Date:       03 July 2020
"""

from src.model.db_manager import DBManager

from src.model.models.units.vehicles import VehiclesCustom, VehiclesDefault
from src.model.models.units.infantry import InfantryCustom, InfantryDefault
from src.model.models.units.buildings import BuildingsCustom, BuildingsDefault
from src.model.models.units.ships import ShipsCustom, ShipsDefault
from src.model.models.units.aircraft import AircraftCustom, AircraftDefault


class CoreDBHelper(DBManager):

    def get_change_records(self, default_table, custom_table):
        """
        Finds the differences between the default and custom settings database tables and generates a dictionary of
        items where there is a difference. The values used for the resulting dictionary are taken from the custom
        settings dict.

        :param default_table: The default database table to compare.
        :param custom_table: The custom database table to compare.
        :return: A dictionary of items taken from the custom table where the values differ from the defaults.
        """
        generator = self.__get_comparison_generator(default_table=default_table, custom_table=custom_table)

        items = []
        for custom_record, default_record in generator:
            # Find the differences between the tables.
            diff = set(default_record.items()) ^ set(custom_record.items())
            diff = [item[0] for item in diff]

            # Create a dict of the differing records based on the custom table.
            diff_dict = {key: custom_record[key] for key in diff}

            # If the dict contains items, add the tag and name also for INI creation later.
            if len(diff_dict):
                diff_dict.update({
                    "Tag": custom_record["Tag"],
                    "Name": custom_record["Name"]
                })

                items.append(diff_dict)

        return items

    def __get_comparison_generator(self, default_table, custom_table):
        """
        Creates two lists of dictionaries, one for the game defaults and the other for the current custom user settings.
        The two results are zipped and returned to be used in an iteration loop i.e. for.

        :param default_table: The default game settings table.
        :param custom_table: The custom game settings table.
        :return: A generator for custom and default records zipped together.
        """
        default_records = self.__get_records_as_dictionary_list(table=default_table)
        custom_records = self.__get_records_as_dictionary_list(table=custom_table)

        return zip(custom_records, default_records)

    def __get_records_as_dictionary_list(self, table):
        """
        Converts a database "SELECT * FROM table" result into a list of dictionary items of the same results.
        The feature "_sa_instance_state" is stripped from the results.

        :param table: The table to run the "SELECT * FROM table" on.
        :return: A list of dictionaries, where each dictionary is a row in the database table passed.
        """
        records = self.all(table)
        records = [record.__dict__ for record in records]

        for idx, record in enumerate(records):
            record.pop("_sa_instance_state")

        return records

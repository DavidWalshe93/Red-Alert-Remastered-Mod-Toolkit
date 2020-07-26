"""
Author:     David Walshe
Date:       26 July 2020
"""

import os
import pprint
from configparser import ConfigParser

# Database utils
from src.model.db_utils import get_all_db_table_pairs, table_from_string


class Linker:

    def __init__(self, model):
        self.model = model
        self._tables = get_all_db_table_pairs()
        self.linked_data = {}

    def link(self):
        """
        :return:
        """
        for default, custom in self._tables:
            self.linked_data.update(self.compare_custom_vs_default(default, custom))

        return self.linked_data

    def compare_custom_vs_default(self, default_table, custom_table) -> dict:
        """
        Checks the custom vs the default_table dictionary to see if they are different.

        :return: The names of the items that are different.
        """
        # Get the table class name.
        custom_table_name = str(custom_table).split(".")[-1].replace("'>", "")

        # Get each tables data to compare.
        default_data = self.clean_table_data(default_table)
        custom_data = self.clean_table_data(custom_table)

        data = self.compare(default_data, custom_data)

        compile_data = {
            custom_table_name: data
        }

        return compile_data

    def clean_table_data(self, table) -> list:
        """
        Clean the table data and removed non-required fields from the results.

        :param table: The table to run the query off.
        :return: The cleaned table query data.
        """
        remove_list = ["Id", "_sa_instance_state"]
        data = self.model.query(table)

        data = [item.__dict__ for item in data]

        for item in data:
            # Filter out remove list from each item.
            [item.pop(remove_item) for remove_item in remove_list]

        return data

    @staticmethod
    def compare(default_data, custom_data):
        """
        Compares data between the default and custom data.

        :param default_data: The data of the default table.
        :param custom_data: The data of the custom table.
        :return: The difference between two tables.
        """
        data = {}

        # For each data point.
        for default, custom in zip(default_data, custom_data):

            # XOR operation to keep only elements that are different.
            unmatched_items = set(default.items()) ^ set(custom.items())

            # If there is a difference.
            if len(unmatched_items):
                fields = []
                # Get the name of the feature that is different.
                for item in unmatched_items:
                    fields.append(item[0])

                data.update({
                    custom["Name"]: list(set(fields))
                })

        return data


class Compiler:

    NURPLE_POSTFIX = "_nurple_mod.mpr"

    def __init__(self, model, map_directory):
        print("Compiler created")
        self.model = model
        self.mpr_directory = map_directory
        self.out_file_name = map_directory

        self.linker = Linker(self.model)

        self.writer = ConfigParser(allow_no_value=True)
        self.writer.optionxform = str

    def write(self):
        print("Writing")
        for mpr_file in self.mpr_files:
            print(mpr_file)
            with open(mpr_file) as fh:
                content = fh.read()

            out_file = self.output_file_name(mpr_file)
            with open(out_file, "w") as fh:
                self.writer.write(fh)
                fh.write(content)

    def build(self):
        for key, data in self.linker.linked_data.items():
            table = table_from_string(key)

            for name, fields in data.items():
                # Get Data.
                query = self.model.query_first(table, Name=name).__dict__

                # Add Section
                section = query["Tag"]
                self.writer.add_section(section)

                # Add Options and values
                for field in fields:
                    self.writer.set(section, field, str(query[field]))

    def compile(self):
        self.linker.link()
        self.build()
        self.write()

    def output_file_name(self, file_name: str) -> str:
        out_file = ".".join(file_name.split(".")[:-1])
        out_file = f"{out_file}{self.NURPLE_POSTFIX}"

        return out_file

    @property
    def mpr_files(self) -> list:
        """
        Get all the mpr file paths to use for the mod adding.

        :return: A list of file paths for .mpr files in the chosen map directory.
        """
        try:
            mpr_files = os.listdir(self.mpr_directory)
            mpr_files = [os.path.join(self.mpr_directory, file) for file in mpr_files if file.endswith(".mpr")]
            mpr_files = [file for file in mpr_files if file.find(self.NURPLE_POSTFIX) == -1]

            return mpr_files

        except OSError as err:
            logger.error(f"Could not get map directory contents.\n\t"
                         f"User config: {ConfigManager().config}\n\t"
                         f"{err}")

            return []
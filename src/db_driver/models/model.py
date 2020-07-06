"""
Author:     David Walshe
Date:       06 July 2020
"""

from src.db_driver.connection_manager import ConnectionManager

Base = ConnectionManager.base()


class Model:

    def insert_from_dict(self, item: dict):
        """
        Helper method to insert a dict object
        :param item:
        :return:
        """
        attribute_names = [attrib for attrib in dir(self) if attrib[0].isupper()]

        new_item = {**self.__dict__, **item}

        for name in attribute_names:
            try:
                self.__setattr__(name, new_item[name])
            except KeyError:
                pass

    @classmethod
    def property_names(cls) -> dict:
        """
        Helper method to return all class attribute names (Table Column Names) back in snake case to access as
        properties in controller code.

        :return: A list of snake_case property names matching those of the database column names.
        """
        # Get all the Column attributes
        column_names = [name for name in dir(cls) if name[0].isupper()]

        property_names = []

        for name in column_names:
            # Check to see if the name is an abbreviation i.e. ROT
            is_all_upper = [1 if letter.isupper() else 0 for letter in name[1:]]

            # If not an abbreviation
            if min(is_all_upper) == 0:
                # place a underscore in front of every capital, starting after the first letter.
                letters = [f"_{letter}" if letter.isupper() else letter for letter in name[1:]]
                # join the result and lowercase all letters to create snake case format.
                property_names.append(name[0].lower() + "".join(letters).lower())
            else:
                # lower case the abbreviation.
                property_names.append(name.lower())

        return {column_name: property_name for column_name, property_name in zip(column_names, property_names)}

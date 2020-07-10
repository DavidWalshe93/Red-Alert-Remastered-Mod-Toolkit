"""
Author:     David Walshe
Date:       06 July 2020
"""

from src.model.connection_manager import ConnectionManager

Base = ConnectionManager.base()


class Model:

    @classmethod
    def mapping(cls) -> dict:
        return {}

    @classmethod
    def inverse_mapping(cls) -> dict:
        mapping = cls.mapping()
        return {mapping[key]: key for key in mapping.keys()}

    @classmethod
    def mapping_keys(cls) -> list:
        return list(cls.mapping().keys())

    @classmethod
    def inv_mapping_keys(cls) -> list:
        return list(cls.inverse_mapping().keys())

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
            # lower case the abbreviation.
            if name in cls.mapping():
                property_names.append(cls.mapping()[name])
            else:
                # place a underscore in front of every capital, starting after the first letter.
                letters = [f"_{letter}" if letter.isupper() else letter for letter in name[1:]]
                # join the result and lowercase all letters to create snake case format.
                property_names.append(name[0].lower() + "".join(letters).lower())

        return {column_name: property_name for column_name, property_name in zip(column_names, property_names)}

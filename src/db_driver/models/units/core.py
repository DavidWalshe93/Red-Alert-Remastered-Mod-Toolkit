"""
Author:     David Walshe
Date:       28 June 2020
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db_driver.connection_manager import ConnectionManager

Base = ConnectionManager.base()


class Core:

    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Tag = Column(String, unique=True)
    Ammo = Column(Integer, default=-1)
    Armor = Column(String, default="none")
    Cloakable = Column(String, default="no")
    Cost = Column(Integer, default=1)
    Explodes = Column(String, default="no")
    GuardRange = Column(Integer, nullable=True)
    Image = Column(String, nullable=True)
    Invisible = Column(String, default="no")
    Owner = Column(String, default="allies,soviet")
    Points = Column(Integer, default=0)
    Prerequisite = Column(String, default="no")
    Primary = Column(String, default="none")
    Secondary = Column(String, default="none")
    ROT = Column(Integer, default=0)
    Reload = Column(Integer, default=0)
    SelfHealing = Column(String, default="no")
    Sight = Column(Integer, default=1)
    Strength = Column(Integer, default=1)
    TechLevel = Column(Integer, default=-1)
    Sensors = Column(String, default="no")
    DoubleOwned = Column(String, default="no")

    def insert_from_dict(self, item: dict):
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


class Unit(Core):

    Passengers = Column(Integer, default=0)
    Speed = Column(Integer, default=0)














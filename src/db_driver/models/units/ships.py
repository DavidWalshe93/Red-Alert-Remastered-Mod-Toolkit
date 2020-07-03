"""
Author:     David Walshe
Date:       02 July 2020
"""

from src.db_driver.models.units.core import Unit, Base, Column, String, Integer


class Ships(Unit):
    pass


class ShipsDefault(Base, Ships):

    __tablename__ = "ships_defaults"


class ShipsCustom(Base, Ships):

    __tablename__ = "ship_customs"

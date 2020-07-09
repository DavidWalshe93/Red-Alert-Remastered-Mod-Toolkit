"""
Author:     David Walshe
Date:       02 July 2020
"""

from src.db_driver.models.units.core import Unit, Base, Column, String, Integer


class Infantry(Unit):

    C4 = Column(String, default="no")
    Fraidycat = Column(String, default="no")
    Infiltrate = Column(String, default="no")
    IsCanine = Column(String, default="no")


class InfantryDefault(Base, Infantry):

    __tablename__ = "infantry_default"


class InfantryCustom(Base, Infantry):

    __tablename__ = "infantry_custom"

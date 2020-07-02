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

class Unit(Core):

    Passengers = Column(Integer, default=0)
    Speed = Column(Integer, default=0)


class Infantry(Base, Unit):

    __tablename__ = "infantry"

    C4 = Column(String, default="no")
    Fraidycat = Column(String, default="no")
    Infiltrate = Column(String, default="no")
    IsCanine = Column(String, default="no")


class Vehicles(Base, Unit):

    __tablename__ = 'vehicles'

    Crushable = Column(String, default="no")
    Tracked = Column(String, default="no")
    NoMovingFire = Column(String, default="no")


class Aircraft(Base, Unit):

    __tablename__ = "aircraft"


class Ships(Base, Unit):

    __tablename__ = "ships"


class Buildings(Base, Core):

    __tablename__ = "buildings"

    BaseNormal = Column(String, default="yes")
    Adjacent = Column(Integer, default=1)
    Bib = Column(String, default="no")
    Capturable = Column(String, default="yes")
    Crewed = Column(String, default="no")
    Power = Column(Integer, default=0)
    Powered = Column(String, default="no")
    Repairable = Column(String, default="yes")
    Storage = Column(Integer, default=0)
    Unsellable = Column(String, default="no")
    WaterBound = Column(String, default="no")

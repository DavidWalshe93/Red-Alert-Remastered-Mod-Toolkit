"""
Author:     David Walshe
Date:       28 June 2020
"""


from sqlalchemy import Column, Integer, String

from src.model.models.model import Model, Base


class Core(Model):

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

    @classmethod
    def mapping(cls):
        return {
            "ROT": "rot"
        }


class Unit(Core):

    Passengers = Column(Integer, default=0)
    Speed = Column(Integer, default=0)














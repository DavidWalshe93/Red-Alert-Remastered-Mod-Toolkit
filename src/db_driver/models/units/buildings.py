"""
Author:     David Walshe
Date:       02 July 2020
"""

from src.db_driver.models.units.core import Core, Base, Column, String, Integer


class Buildings(Core):
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


class BuildingsDefault(Base, Buildings):

    __tablename__ = "building_defaults"


class BuildingsCustom(Base, Buildings):

    __tablename__ = "building_custom"
"""
Author:     David Walshe
Date:       02 July 2020
"""

from src.db_driver.models.units.core import Unit, Base, Column, String, Integer


class Vehicles(Unit):
    Crushable = Column(String, default="no")
    Tracked = Column(String, default="no")
    NoMovingFire = Column(String, default="no")


class VehiclesDefault(Base, Vehicles):
    __tablename__ = "vehicles_default"


class VehiclesCustom(Base, Vehicles):
    __tablename__ = "vehicles_custom"

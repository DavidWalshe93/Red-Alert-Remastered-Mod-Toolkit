"""
Author:     David Walshe
Date:       02 July 2020
"""

from src.model.models.units.core import Unit, Base


class Aircraft(Unit):
    pass


class AircraftDefault(Base, Aircraft):
    __tablename__ = "aircraft_default"


class AircraftCustom(Base, Aircraft):
    __tablename__ = "aircraft_custom"

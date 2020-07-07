"""
Author:     David Walshe
Date:       06 July 2020
"""

from sqlalchemy import Column, Integer, String, Float

from src.db_driver.models.model import Model, Base


class Country(Model):
    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Tag = Column(String, unique=True)
    Firepower = Column(Float, default=1.0)
    Groundspeed = Column(Float, default=1.0)
    Airspeed = Column(Float, default=1.0)
    Armor = Column(Float, default=1.0)
    ROF = Column(Float, default=1.0)
    Cost = Column(Float, default=1.0)
    BuildTime = Column(Float, default=1.0)


class CountryDefaults(Country, Base):
    __tablename__ = "country_defaults"


class CountryCustom(Country, Base):
    __tablename__ = "country_custom"

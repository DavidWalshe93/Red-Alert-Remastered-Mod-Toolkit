"""
Author:     David Walshe
Date:       29 June 2020
"""
import os
import logging

from src.ini_creator.parser.parser import IniParser
from src.model.db_manager import DBManager
from src.model.models.units.buildings import BuildingsDefault, BuildingsCustom
from src.model.models.units.aircraft import AircraftDefault, AircraftCustom
from src.model.models.units.infantry import InfantryDefault, InfantryCustom
from src.model.models.units.ships import ShipsDefault, ShipsCustom
from src.model.models.units.vehicles import VehiclesDefault, VehiclesCustom
from src.model.models.countries import CountryDefaults, CountryCustom
from src.model.models.general import GeneralDefaults, GeneralCustom

logger = logging.getLogger(__name__)


def add_data(file_name: str, table_cls):
    db = DBManager()
    parser = IniParser()
    data = parser.parse_file(file_name)
    for item in data:
        db.create(table_cls=table_cls, data=item)


def reset_database():
    logger.info(f"Resetting database back to defaults...")
    db = DBManager()
    try:
        db.drop_all()
        db.init_tables()
    except Exception as err:
        logger.error(f"Database population failed - {err}")

    base_path = os.environ["RA_RESOURCE_PATH"]

    res_list = [
        ("unit_statistics/buildings.ini", BuildingsDefault),
        ("unit_statistics/buildings.ini", BuildingsCustom),
        ("unit_statistics/aircraft.ini", AircraftDefault),
        ("unit_statistics/aircraft.ini", AircraftCustom),
        ("unit_statistics/vehicles.ini", VehiclesDefault),
        ("unit_statistics/vehicles.ini", VehiclesCustom),
        ("unit_statistics/infantry.ini", InfantryDefault),
        ("unit_statistics/infantry.ini", InfantryCustom),
        ("unit_statistics/ships.ini", ShipsDefault),
        ("unit_statistics/ships.ini", ShipsCustom),
        ("country_statistics.ini", CountryDefaults),
        ("country_statistics.ini", CountryCustom),
        ("general.ini", GeneralDefaults),
        ("general.ini", GeneralCustom)
    ]

    for path, orm in res_list:
        add_data(f"{base_path}/{path}", orm)

    logger.info(f"Database reset")


def get_all_db_table_pairs():
    return [
        (AircraftDefault, AircraftCustom),
        (BuildingsDefault, BuildingsCustom),
        (InfantryDefault, InfantryCustom),
        (ShipsDefault, ShipsCustom),
        (VehiclesDefault, VehiclesCustom),
        (CountryDefaults, CountryCustom),
        (GeneralDefaults, GeneralCustom)
    ]


if __name__ == '__main__':
    reset_database()

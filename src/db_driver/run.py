"""
Author:     David Walshe
Date:       29 June 2020
"""
import os

os.environ["RA_DB_LOCATION"] = "../../db/red_alert_data.db"

from src.ini_creator.parser.ini_parser import IniParser
from src.db_driver.db_manager import DBManager
from src.db_driver.models.units.buildings import BuildingsDefault, BuildingsCustom
from src.db_driver.models.units.aircraft import AircraftDefault, AircraftCustom
from src.db_driver.models.units.infantry import InfantryDefault, InfantryCustom
from src.db_driver.models.units.ships import ShipsDefault, ShipsCustom
from src.db_driver.models.units.vehicles import VehiclesDefault, VehiclesCustom


def add_data(file_name: str, table_cls):
    db = DBManager()
    parser = IniParser()
    data = parser.parse(file_name)
    for item in data:
        db.create(table_cls=table_cls, data=item)
    print(db.all(table_cls))


def main():
    db = DBManager()
    try:
        pass
        db.drop_all()
        db.init_tables()
    except:
        print("Issue")

    add_data("buildings.ini", BuildingsDefault)
    add_data("buildings.ini", BuildingsCustom)
    add_data("aircraft.ini", AircraftDefault)
    add_data("aircraft.ini", AircraftCustom)
    add_data("vehicles.ini", VehiclesDefault)
    add_data("vehicles.ini", VehiclesCustom)
    add_data("infantry.ini", InfantryDefault)
    add_data("infantry.ini", InfantryCustom)
    add_data("ships.ini", ShipsDefault)
    add_data("ships.ini", ShipsCustom)


if __name__ == '__main__':
    main()
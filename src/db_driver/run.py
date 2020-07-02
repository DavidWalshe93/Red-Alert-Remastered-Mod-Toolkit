"""
Author:     David Walshe
Date:       29 June 2020
"""
import os

os.environ["RA_DB_LOCATION"] = "../../db/defaults.db"

from src.ini_creator.parser.ini_parser import IniParser
from src.db_driver.db_manager import DBManager
from src.db_driver.models.units import Aircraft, Infantry, Vehicles, Ships, Buildings


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
        db.create_all()
    except:
        pass

    add_data("buildings.ini", Buildings)
    add_data("aircraft.ini", Aircraft)
    add_data("vehicles.ini", Vehicles)
    add_data("infantry.ini", Infantry)
    add_data("ships.ini", Ships)


if __name__ == '__main__':
    main()
"""
Author:     David Walshe
Date:       27 June 2020
"""

from src.ini_creator.parser.ini_parser import IniParser


class UnitParser(IniParser):

    def __init__(self):
        """

        """
        super().__init__()

    @property
    def defaults(self) -> dict:
        return {
            "Ammo": -1,
            "Armor": "none",
            "Cloakable": "no",
            "Cost": 1,
            "Explodes": "no",
            "GuardRange": "DEFAULT",
            "Image": "DEFAULT",
            "Invisible": "no",
            "Owner": "allies,soviet",
            "Points": 0,
            "Prerequisite": "DEFAULT",
            "Primary": "none",
            "Secondary": "none",
            "ROT": 0,
            "Reload": 0,
            "SelfHealing": "no",
            "Sight": 1,
            "Strength": "DEFAULT",
            "TechLevel": -1,
            "Sensors": "no",
            "DoubleOwned": "no"
        }

    @property
    def non_buildings(self):
        return {
            "Speed": 0,
            "Passengers": 0,
        }

    @property
    def vehicles(self):
        return {
            **defaults(),
            **non_buildings(),
            "Crushable": "no",
            "Tracked": "no",
            "NoMovingFire": "no"
        }

    @property
    def infantry(self):
        return {
            **defaults(),
            **non_buildings(),
            "C4": "no",
            "Fraidycat": "no",
            "Infiltrate": "no",
            "IsCanine": "no"
        }

    @property
    def buildings(self):
        return {
            **defaults(),
            "BaseNormal": "yes",
            "Adjacent": "yes",
            "Bib": "no",
            "Capturable": "no",
            "Crewed": "no",
            "Power": 0,
            "Powered": "no",
            "Repairable": "yes",
            "Storage": 0,
            "Unsellable": "no",
            "WaterBound": "no"
        }

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
    def defaults(self):
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

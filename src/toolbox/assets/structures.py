"""
Author:     David Walshe
Date:       30 July 2020
"""

"""
Author:     David Walshe
Date:       26 June 2020
"""

import time
import functools

import pyautogui as ui

from src.toolbox.toolbox import Toolbox


def select_asset(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper to select asset before drawing.
        """
        print(kwargs)
        self.asset = kwargs.pop("asset")
        self.player = kwargs.pop("player")

        # Open the resources Toolbar.
        ui.click(*self.toolbar.resources)
        ui.click(*self.toolbar.structures)
        ui.moveTo(*self.option_box)
        ui.click()

        # Scroll down options
        ui.moveTo(*self.scroll_down_location)
        for i in range(self.option_scroll_list[self.asset]):
            ui.click()

        ui.moveTo(*self.option)
        ui.click()

        ui.click(self.house_box)
        ui.click(self.players_options[self.player])

        return method(self, *args, **kwargs)

    return wrapper


class Structures(Toolbox):

    def __init__(self, *args, **kwargs):
        """
        Places a wall in the Map Builder App.
        """
        super().__init__(*args, **kwargs)
        self.option_box = (262, 124)
        self.scroll_down_location = (262, 703)
        self.option = (130, 148)
        self.house_box = (259, 383)
        self.players_options = {
            "P0": (105, 555),
            "P1": (105, 567),
            "P2": (105, 583),
            "P3": (105, 595),
            "P4": (105, 601),
            "P5": (105, 611),
            "P6": (105, 621),
            "P7": (105, 635),
        }
        self.__player = self.players_options["P0"]
        self.__asset = self.ADV_POWER_PLANT
        self.option_scroll_list = {
            self.AA_GUN: 1,
            self.ADV_POWER_PLANT: 2,
            self.RADAR_DOME: 8,
            self.CONSTRUCTION_YARD: 9,
            self.SERVICE_DEPOT: 11,
            self.FLAME_THROWER: 12,
            self.GAP_GENERATOR: 13,
            self.TURRET: 14,
            self.CAMO_PILLBOX: 15,
            self.POWER_PLANT: 28,
            self.REFINERY: 29,
            self.SAM: 31,
            self.SILO: 32,
            self.TESLA_COIL: 37,
            self.WAR_FACTORY: 50
        }

    @property
    def ADV_POWER_PLANT(self):
        return "adv_power_plant"

    @property
    def AA_GUN(self):
        return "aa_gun"

    @property
    def RADAR_DOME(self):
        return "radar_dome"

    @property
    def CONSTRUCTION_YARD(self):
        return "construction_yard"

    @property
    def SERVICE_DEPOT(self):
        return "service_depot"

    @property
    def FLAME_THROWER(self):
        return "flame_thrower"

    @property
    def GAP_GENERATOR(self):
        return "gap_generator"

    @property
    def TURRET(self):
        return "turret"

    @property
    def CAMO_PILLBOX(self):
        return "camo_pillbox"

    @property
    def POWER_PLANT(self):
        return "power_plant"

    @property
    def REFINERY(self):
        return "refinery"

    @property
    def SAM(self):
        return "sam"

    @property
    def SILO(self):
        return "silo"

    @property
    def TESLA_COIL(self):
        return "tesla_coil"

    @property
    def WAR_FACTORY(self):
        return "war_factory"

    @property
    def asset(self):
        return self.__asset

    @asset.setter
    def asset(self, value):
        if value not in list(self.option_scroll_list.keys()):
            raise ValueError("Non-exist 'Structure' option set")

        self.__asset = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        if value not in list(self.players_options.keys()):
            raise ValueError("Non-exist 'Player' option set")

        self.__player = value

    @select_asset
    def draw(self, *args, **kwargs) -> None:
        """
        Helper method to call the correct draw method on the canvas.
        """
        print(args)
        print(kwargs)
        super().draw((*args, *args), **kwargs, force_replace=True)


if __name__ == '__main__':
    ui.alert("Press ok when the App Builder is in the foreground.")
    structures = Structures()

    offset = 10
    structures.draw(100, 40, asset=structures.RADAR_DOME, player="P2")

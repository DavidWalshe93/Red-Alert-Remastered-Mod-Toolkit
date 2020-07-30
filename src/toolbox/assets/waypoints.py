"""
Author:     David Walshe
Date:       28 July 2020
"""

import pyautogui as ui

from src.toolbox.toolbox import Toolbox


class WayPoints(Toolbox):

    def __init__(self):
        super().__init__()
        self.__asset = "P0"
        self.WAYPOINT_DROPDOWN = (135, 125)
        self.PLAYER_X_OPTION = 80
        self.PLAYER_Y_OPTIONS = {
            "P0": 140,
            "P1": 152,
            "P2": 166,
            "P3": 182,
            "P4": 194,
            "P5": 206,
            "P6": 220,
            "P7": 232,
        }

    @property
    def asset(self):
        return self.__asset

    @asset.setter
    def asset(self, value):
        if value not in list(self.PLAYER_Y_OPTIONS.keys()):
            raise ValueError("Non-exist 'Waypoint' option set")

        self.__asset = value

    def select_asset(self):
        # Select Waypoint option
        ui.click(*self.toolbar.resources)
        ui.click(*self.toolbar.waypoints)

        # Select Dropdown
        ui.click(*self.WAYPOINT_DROPDOWN)
        ui.click(self.PLAYER_X_OPTION, self.PLAYER_Y_OPTIONS[self.asset])

    def draw(self, route, asset: str = "P0"):
        self.asset = asset
        self.select_asset()

        super().draw((*route, *route))


if __name__ == '__main__':
    WayPoints().draw((40, 30))

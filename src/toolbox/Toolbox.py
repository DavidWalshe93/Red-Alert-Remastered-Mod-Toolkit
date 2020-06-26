"""
Author:     David Walshe
Date:       26 June 2020
"""

from abc import ABC, abstractmethod

import pyautogui as ui


class Toolbox(ABC):
    BASE_ASSET_SIZE = 7
    X_START = 502
    Y_START = 89

    def __init__(self, x_max: int = 115, y_max: int = 132):
        """
        Class constructor.

        :param x_max: The maximum X size of the canvas.
        :param y_max: The maximum Y size of the canvas.
        """
        self.x_max = x_max
        self.y_max = y_max
        self.asset_width = 1
        self.asset_length = 1
        self.toolbar_y_location = 62
        self.toolbar_x_locations = {
            "map": 43,
            "smudge": 115,
            "overlay": 192,
            "terrain": 270,
            "infantry": 334,
            "unit": 400,
            "structures": 470,
            "resources": 565,
            "walls": 640,
            "waypoints": 724,
            "cell_triggers": 800
        }

    def x_map(self, coordinate: int) -> int:
        """
        Maps a cell X coordinate to a y-axis pixel coordinate for the map builder app.

        :param coordinate: The x-cell coordinate to map.
        :return: The mapped x-pixel coordinate.
        """
        if 0 > coordinate > self.x_max:
            raise ValueError("X-Grid only can be 0 to 115")

        print(self.asset_width)
        return coordinate * self.BASE_ASSET_SIZE + self.X_START + (self.BASE_ASSET_SIZE * self.asset_width)

    def y_map(self, coordinate: int) -> int:
        """
        Maps a cell Y coordinate to a y-axis pixel coordinate for the map builder app.

        :param coordinate: The y-cell coordinate to map.
        :return: The mapped y-pixel coordinate.
        """
        if 0 > coordinate > self.y_max:
            raise ValueError("Y-Grid only can be 0 to 132")
        print(self.asset_length)
        return coordinate * self.BASE_ASSET_SIZE + self.Y_START + (self.BASE_ASSET_SIZE * self.asset_length)

    @property
    def structures(self):
        return self.toolbar_x_locations["structures"], self.toolbar_y_location

    @property
    def resources(self):
        return self.toolbar_x_locations["resources"], self.toolbar_y_location

    @abstractmethod
    def select_asset(self):
        """
        Abstract method to be implemented to select a resource from the Map Builder app.
        """
        pass

    def draw(self, route: tuple, force_replace: bool = False):
        """
        Implemented to draw on the Map Builder app canvas.
        """

        ui.keyDown("shift")

        if force_replace:
            self.__draw(route, "RIGHT")
        self.__draw(route, "LEFT")

        ui.keyUp("shift")

    def __draw(self, route: tuple, button: str = "LEFT"):
        x_from, y_from, x_to, y_to = route

        ui.click(x_from, y_from)
        for y in range(y_from, y_to):
            for x in range(x_from, x_to):
                if y % self.asset_length == 0 and x % self.asset_width == 0:
                    ui.click(self.x_map(x), self.y_map(y), button=button)
                    print(f"Working on {x}, {y} cell")

        ui.click(button=button)

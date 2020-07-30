"""
Author:     David Walshe
Date:       26 June 2020
"""

from abc import ABC, abstractmethod

import pyautogui as ui

from src.toolbox.toolbar import Toolbar


class Toolbox(ABC):

    BASE_ASSET_SIZE = 7.3
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
        self.toolbar = Toolbar()

    def x_map(self, coordinate: int) -> int:
        """
        Maps a cell X coordinate to a y-axis pixel coordinate for the map builder app.

        :param coordinate: The x-cell coordinate to map.
        :return: The mapped x-pixel coordinate.
        """
        if 0 > coordinate > self.x_max:
            raise ValueError("X-Grid only can be 0 to 115")

        return round(coordinate * self.BASE_ASSET_SIZE + self.X_START + (self.BASE_ASSET_SIZE * self.asset_width))

    def y_map(self, coordinate: int) -> int:
        """
        Maps a cell Y coordinate to a y-axis pixel coordinate for the map builder app.

        :param coordinate: The y-cell coordinate to map.
        :return: The mapped y-pixel coordinate.
        """
        if 0 > coordinate > self.y_max:
            raise ValueError("Y-Grid only can be 0 to 132")

        return round(coordinate * self.BASE_ASSET_SIZE + self.Y_START + (self.BASE_ASSET_SIZE * self.asset_length))

    def select_asset(self):
        """
        Abstract method to be implemented to select a resource from the Map Builder app.
        """
        pass

    def draw(self, route: tuple, force_replace: bool = False, remove: bool = False):
        """
        Implemented to draw on the Map Builder app canvas.
        """
        ui.keyDown("shift")

        if force_replace:
            self.__draw(route, "RIGHT")

        if remove:
            self.__draw(route, "RIGHT")
        else:
            self.__draw(route, "LEFT")

        ui.keyUp("shift")

    def __draw(self, route: tuple, button: str = "LEFT") -> None:
        """
        Draws on the Map Builder canvas. Content to be draw is predefined in subclass.

        :param route: The route to draw from and to. (X1, Y1, X2, Y2)
        :param button: The button to use for the pattern, LEFT-Draw, RIGHT-Remove.
        """
        x_from, y_from, x_to, y_to = route

        ui.click(self.x_map(x_from), self.y_map(y_from))
        for y in range(y_from, y_to):
            for x in range(x_from, x_to):
                if y % self.asset_length == 0 and x % self.asset_width == 0:
                    ui.click(self.x_map(x), self.y_map(y), button=button)
                    print(f"Working on {x}, {y} cell")

        ui.click(button=button)

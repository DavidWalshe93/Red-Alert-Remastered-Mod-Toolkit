"""
Author:     David Walshe
Date:       26 June 2020
"""

import time

import pyautogui as ui

from src.toolbox.toolbox import Toolbox


class Walls(Toolbox):

    def __init__(self, *args, **kwargs):
        """
        Places a wall in the Map Builder App.
        """
        super().__init__(*args, **kwargs)
        self.wall_option_box = (260, 124)
        self.scroll_down_location = (259, 510)
        self.wall_option = (130, 200)
        self.wall_option_alt = (130, 335)
        self.__asset = self.CONCRETE_WALLS
        self.option_scroll_count = {
            self.BARBED_WIRE: 0,
            self.CONCRETE_WALLS: 1,
            self.CHAIN_FENCE: 2,
            self.WIRE_FENCE: 3,
            self.SANDBAGS: 4,
            self.WOODEN_FENCE: 4
        }

    @property
    def BARBED_WIRE(self):
        return "barbed_wire"

    @property
    def CONCRETE_WALLS(self):
        return "concrete_walls"

    @property
    def CHAIN_FENCE(self):
        return "chain_fence"

    @property
    def WIRE_FENCE(self):
        return "wire_fence"

    @property
    def SANDBAGS(self):
        return "sandbags"

    @property
    def WOODEN_FENCE(self):
        return "wooden_fence"

    @property
    def asset(self):
        return self.__asset

    @asset.setter
    def asset(self, value):
        if value not in list(self.option_scroll_count.keys()):
            raise ValueError("Non-exist 'Wall' option set")

        self.__asset = value

    def select_asset(self):
        """
        Select an asset type form the toolbar and wall palette.
        """
        # Open the resources Toolbar.
        ui.click(*self.toolbar.resources)
        ui.click(*self.toolbar.walls)
        ui.moveTo(*self.wall_option_box)
        ui.click()

        # Scroll down options
        ui.moveTo(*self.scroll_down_location)
        for i in range(self.option_scroll_count[self.asset]):
            ui.click()

        # Select the asset from the options pane.
        if self.asset == self.WOODEN_FENCE:
            ui.moveTo(self.wall_option_alt)
        else:
            ui.moveTo(*self.wall_option)
        ui.click()

    def draw_x(self, start: int, end: int, y_pos: int, asset: str = "concrete_walls") -> None:
        """
        Draw a wall in the x-axis of the Map Builder app.

        :param start: The start location in the x-axis.
        :param end: The end location in the x-axis.
        :param y_pos: The y-axis to place the wall on.
        :param asset: The type of wall asset to use. Default = 'concrete_walls'
        """
        self.asset = asset
        self.select_asset()
        super().draw(route=(start, y_pos, end, y_pos+1))

    def draw_y(self, start: int, end: int, x_pos: int, asset: str = "concrete_walls") -> None:
        """
        Draw a wall in the y-axis of the Map Builder app.

        :param start: The start location in the y-axis.
        :param end: The end location in the y-axis.
        :param x_pos: The x-axis to place the wall on.
        :param asset: The type of wall asset to use. Default = 'concrete_walls'
        """
        self.asset = asset
        self.select_asset()
        super().draw(route=(x_pos, start, x_pos+1, end))

    def draw_clear(self, start: int, end: int, pos: int, orient: str) -> None:
        """
        Clears walls from the map.

        :param start: The start location of the clear.
        :param end:  The end location of the clear.
        :param pos: The axis position.
        :param orient: The orientation or axis (x or y)
        """
        if orient == "x":
            super().draw(route=(start, pos, end, pos + 1), remove=True)
        else:
            super().draw(route=(pos, start, pos+1, end), remove=True)

    def draw(self, *arg, **kwargs) -> None:
        """
        Helper method to call the correct draw method on the canvas.
        """
        print(kwargs)
        orientation = kwargs.pop("orient").lower()
        if orientation == "x":
            kwargs["y_pos"] = kwargs.pop("offset")
            self.draw_x(*arg, **kwargs)
        elif orientation == "y":
            kwargs["x_pos"] = kwargs.pop("offset")
            self.draw_y(*arg, **kwargs)
        else:
            raise ValueError(f"'orient' value must be either 'x' or 'y', found {orientation}")


class BaseWalls:

    def __init__(self):
        """
        Creates a perimeter wall for bases.
        """
        pass

    def get_perimeter(self, x: int, y: int, size: int) -> tuple:
        x1 = x - size
        y1 = y - size
        x2 = x + size
        y2 = y + size

        return x1, y1, x2, y2

    def draw(self, x: int, y: int, size: int, asset: str = "concrete_walls"):
        """
        Draws a perimeter wall for a base.
        """
        walls = Walls()

        x1, y1, x2, y2 = self.get_perimeter(x, y, size)

        walls.draw_x(x1, x2, y1, asset)
        walls.draw_y(y1, y2, x1, asset)
        walls.draw_x(x1, x2, y2, asset)
        walls.draw_y(y1, y2+1, x2, asset)

        x_clear = (x2-x1)//2 + x1
        y_clear = (y2-y1)//2 + y1
        walls.draw_clear(x_clear - 2, x_clear + 2, y1, orient="x")
        walls.draw_clear(x_clear - 2, x_clear + 2, y2, orient="x")
        walls.draw_clear(y_clear - 2, y_clear + 2, x1, orient="y")
        walls.draw_clear(y_clear - 2, y_clear + 2, x2, orient="y")



if __name__ == '__main__':
    ui.alert("Press ok when the App Builder is in the foreground.")
    walls = Walls()

    offset = 10
    walls.draw_x(20, 25, offset, asset=walls.BARBED_WIRE)
    walls.draw_x(20, 25, offset+1)
    walls.draw_x(20, 25, offset+2, asset=walls.CHAIN_FENCE)
    walls.draw_x(20, 25, offset+3, asset=walls.WIRE_FENCE)
    walls.draw_x(20, 25, offset+4, asset=walls.SANDBAGS)
    walls.draw_x(20, 25, offset+5, asset=walls.WOODEN_FENCE)

    walls.draw_y(offset, offset+6, 26, asset=walls.BARBED_WIRE)
    walls.draw_y(offset, offset+6, 26+1)
    walls.draw_y(offset, offset+6, 26+2, asset=walls.CHAIN_FENCE)
    walls.draw_y(offset, offset+6, 26+3, asset=walls.WIRE_FENCE)
    walls.draw_y(offset, offset+6, 26+4, asset=walls.SANDBAGS)
    walls.draw_y(offset, offset+6, 26+5, asset=walls.WOODEN_FENCE)

"""
Author:     David Walshe
Date:       28 July 2020
"""

from src.toolbox.toolbox import Toolbox
from src.toolbox.assets.walls import BaseWalls
from src.toolbox.assets.waypoints import WayPoints
from src.toolbox.assets.structures import Structures


class Base(Toolbox):

    def select_asset(self):
        pass

    def __init__(self):
        """
        Creates a basic base blueprint.
        """
        super().__init__()
        pass

    @staticmethod
    def center_point(**kwargs):
        """Get the center-point for the base"""
        x = (kwargs["x2"] - kwargs["x1"]) // 2 + kwargs["x1"]
        y = (kwargs["y2"] - kwargs["y1"]) // 2 + kwargs["y1"]

        return x, y

    def draw(self, *args, **kwargs):
        """
        Draw the base outline.
        """
        player = kwargs.pop("player")
        if kwargs.get("x2") is not None:
            WayPoints().draw(Base.center_point(**kwargs), player)
        else:
            x = kwargs["x"]
            y = kwargs["y"]
            WayPoints().draw((x, y), player)


class WalledBase(Base):

    def draw(self, *args, **kwargs):
        """
        Draw the base outline with walls.
        """
        super().draw(*args, **kwargs)

        # Remove non-required keys.
        _ = kwargs.pop("player")
        BaseWalls().draw(**kwargs)


class FullBase(WalledBase):

    def draw(self, *args, **kwargs):
        """
        Draw a full base.
        """
        kwargs["size"] = 10
        # super().draw(*args, **kwargs)

        x = kwargs.pop("x")
        y = kwargs.pop("y")
        _ = kwargs.pop("size")

        structures = [
            ("adv_power_plant", (x - 10, y-40)),
            ("adv_power_plant", (x + 7, y)),
            ("adv_power_plant", (x + 21, y)),
            ("adv_power_plant", (x - 10, y + 40)),
            ("adv_power_plant", (x + 7, y + 40)),
            ("adv_power_plant", (x + 21, y + 40))
        ]

        for structure, coords in structures:
            print(structure, coords)
            Structures().draw(*coords, asset=structure, **kwargs)

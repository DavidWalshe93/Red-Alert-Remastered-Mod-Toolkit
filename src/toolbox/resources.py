"""
Author:     David Walshe
Date:       26 June 2020
"""

from math import floor

import pyautogui as ui

from src.toolbox.Toolbox import Toolbox


class Resources(Toolbox):

    def __init__(self, *args, **kwargs):
        """
        Places a resource in the Map Builder App.
        """
        super().__init__(*args, **kwargs)
        self.size = 1

    @staticmethod
    def verify_size(size) -> int:
        """
        Verifies the size of the 'size' argument matches what is available in the Map Builder app.

        :param size: The size (1, 3, 5, 7, 9)
        :return:
        """
        size_conversion = {
            1: 1,
            3: 2,
            5: 3,
            7: 4,
            9: 5
        }
        if size not in (1, 3, 5, 7, 9):
            raise ValueError("'size' for Resources must be set to (1, 3, 5, 7 or 9)")

        return size_conversion[size]

    def select_asset(self) -> None:
        """
        Selects a asset type from the toolbar.
        """
        ui.click(*self.structures)
        ui.click(*self.resources)

    def calculate_size(self, size: int) -> None:
        """
        Calculates the displacement size for the resource ore field.

        :param size: The size of the ore field.
        """
        temp_size = floor(size / 2)

        self.asset_width = temp_size if temp_size > 0 else 1
        self.asset_length = temp_size if temp_size > 0 else 1

        self.size = self.verify_size(size)

    def select_resource_size_incrementer(self) -> None:
        """
        Increments the resource size before placing an ore field.
        """
        self.select_asset()
        ui.moveTo(195, 139)
        for i in range(1, self.size):
            ui.click()

    @staticmethod
    def select_gems_toggle() -> None:
        """
        Selects the gems toggle switch for resource placement.
        """
        ui.moveTo(18, 167)
        ui.click()

    def draw(self, size: int = 1, gems: bool = False, force_replace: bool = False, *args, **kwargs) -> None:
        """
        Draw the resource field in the Map Builder app.

        :param size: The size of the ore field to draw.
        :param gems: Place a gem field instead of ore.
        :param args: The args for draw.
        """
        self.calculate_size(size)
        self.select_resource_size_incrementer()
        if gems:
            self.select_gems_toggle()
        super().draw(force_replace=force_replace, *args, **kwargs)


if __name__ == '__main__':
    ui.alert("Press ok when the App Builder is in the foreground.")
    rs = Resources(9)
    rs.draw(size=9, gems=True, route=(30, 20, 50, 40))
    rs.draw(size=3, gems=False, force_replace=True, route=(30, 20, 40, 25))

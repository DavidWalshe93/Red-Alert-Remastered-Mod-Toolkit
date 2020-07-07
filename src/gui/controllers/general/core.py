"""
Author:     David Walshe
Date:       06 July 2020
"""


from abc import ABC
from src.gui.controllers.contoller import Controller


class CoreController(Controller, ABC):

    def populate_data(self, result: any) -> None:
        super().populate_data(result)

    @property
    def name(self):
        return "General"

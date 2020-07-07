"""
Author:     David Walshe
Date:       06 July 2020
"""

from abc import ABC, abstractmethod
from src.gui.controllers.general.core import CoreController
from src.db_driver.models.general import General


class CombatController(CoreController, ABC):
    pass
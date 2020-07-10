"""
Author:     David Walshe
Date:       06 July 2020
"""

from abc import ABC, abstractmethod
from src.controllers.general.core import CoreController
from src.model.models.general import General


class CombatController(CoreController, ABC):
    pass
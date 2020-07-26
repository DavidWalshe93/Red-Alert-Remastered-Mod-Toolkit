"""
Author:     David Walshe
Date:       29 June 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from abc import ABC, abstractmethod
import logging
import functools

from src.model.db_manager import DBManager
from src.config.config_manager import ConfigManager

if TYPE_CHECKING:
    from src.gui import MainWindow


logger = logging.getLogger(__name__)


def non_none_return_value(func: callable) -> callable:
    """
    Wraps a function in a check to see if the function returns non-None value. If None, raise an error.

    :raise ValueError: If the return value is None.
    :return: The wrapped function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return_value = func(*args, **kwargs)

        if return_value is None:
            logger.error(f"None value is not allowed for {func} with *args {args} and **kwargs {kwargs}")
            raise ValueError("None value is not allowed here")

        return return_value

    return wrapper


class Controller(ABC):

    def __init__(self, view: MainWindow, model: DBManager):
        """
        Base controller to be subclassed.

        :param view: The view object to use.
        """
        self.view = view
        self.model = model
        self.config_manager = ConfigManager()

        self._value = False

    @abstractmethod
    def populate_data(self, result: any = None) -> None:
        """
        Abstract method to be used to populated fields on loading and usage.

        :param result: The data to use to populate the data.
        """
        pass

    @abstractmethod
    @non_none_return_value
    def get_custom_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        pass

    @abstractmethod
    @non_none_return_value
    def get_default_table(self, key):
        """
        Returns the ORM Table object that matches the value key passed.

        :param key: The text key to match the database table to.
        :return: The database ORM Table object.
        """
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def table(self):
        pass

    @abstractmethod
    def tables(self):
        pass

    @property
    def value(self) -> any:
        """
        Returns the value of a widget via a property getter attribute.

        :return: The value of the property.
        """
        if self._value is False:
            logger.error(f"Controller value attribute must not be None")
            raise ValueError("Controller value attribute must not be None")

        return self._value

    @value.setter
    def value(self, attribute: str) -> None:
        """
        :param attribute: The property name to lookup.
        """
        self._value = self.__getattribute__(attribute)

"""
Author:     David Walshe
Date:       03 July 2020
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5 import QtWidgets


def is_checked(checkbox: QtWidgets.QCheckBox):
    """
    Helper method to translate a boolean value from True/False to a yes/no equivalent.

    :param checkbox: The checkbox instance to translate.
    :return: A string representation (yes/no) of a boolean value (True/False).
    """
    return "yes" if checkbox.isChecked() else "no"


def is_checked_true(checkbox: QtWidgets.QCheckBox):
    """
    Helper method to translate a boolean value from True/False to a true/no equivalent.

    Special case for building -> Capturable field

    :param checkbox: The checkbox instance to translate.
    :return: A string representation (true/no) of a boolean value (True/False).
    """
    return "true" if checkbox.isChecked() else "no"


def set_checked(value) -> bool:
    """
    Helper method to translate a database value of yes/no to its boolean equivalent.

    :param value: The value to translate.
    :return: A bool representing True (yes) or False (no)
    """
    return True if value.lower() in ["yes", "true"] else False

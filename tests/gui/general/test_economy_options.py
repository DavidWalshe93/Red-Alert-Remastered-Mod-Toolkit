"""
Author:     David Walshe
Date:       26 July 2020
"""

import os
import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from tests.gui.utilities import min_value_spinbox, max_value_spinbox, step_value_spinbox, check_box_checked, check_box_unchecked

app = QApplication([])


# ======================================================================================================================
# SpinBox Tests
# ======================================================================================================================


def get_spinbox_data():
    return [
        # Widget Name       Min Max Step
        ("bailCountSpinBox", 1, 100, 1),
        ("buildSpeedSpinBox", 0.05, 3.0, 0.05),
        ("goldValueSpinBox", 5, 1000, 5),
        ("gemValueSpinBox", 5, 2500, 5),
        ("growthRateDoubleSpinBox", 0.05, 4.0, 0.05),
        ("oreTruckRateSpinBox", 0.05, 3.0, 0.05),
        ("survivorRateSpinBox", 0.00, 5.0, 0.1),
    ]


def get_spinbox_names():
    return [widget[0] for widget in get_spinbox_data()]


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_min_value_spinbox(gui, widget_data: tuple):
    assert min_value_spinbox(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_max_value_spinbox(gui, widget_data: tuple):
    assert max_value_spinbox(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_step_value_spinbox(gui, widget_data: tuple):
    assert step_value_spinbox(gui, widget_data)


# ======================================================================================================================
# Check Box Tests
# ======================================================================================================================


def get_check_box_data():
    return [
        # Widget name
        "oreGrowsCheckBox",
        "oreSpreadsCheckBox",
        "separateAircraftCheckBox"
    ]


@pytest.mark.parametrize("widget_data", get_check_box_data())
def test_check_box_checked(gui, widget_data: str):
    assert check_box_checked(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_check_box_data())
def test_check_box_unchecked(gui, widget_data: str):
    assert check_box_unchecked(gui, widget_data)

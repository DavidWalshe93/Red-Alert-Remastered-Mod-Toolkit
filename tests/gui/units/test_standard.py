"""
Author:     David Walshe
Date:       26 July 2020
"""

import pytest
from tests.gui.utilities import min_value_spinbox, max_value_spinbox, step_value_spinbox, check_box_checked, \
    check_box_unchecked, verify_combo_box_changes


# ======================================================================================================================
# SpinBox Tests
# ======================================================================================================================

def get_spinbox_data() -> list:
    return [
        # Widget Name   Min Max Step
        ("ammoSpinBox", -1, 10, 1),
        ("costSpinBox", 50, 10_000, 50),
        ("guardRangeSpinBox", 0, 100, 1),
        ("pointsSpinBox", 0, 1000, 1),
        ("rotSpinBox", 0, 10, 1),
        ("reloadSpinBox", 0, 99, 1),
        ("sightSpinBox", 0, 20, 1),
        ("strengthSpinBox", 1, 2000, 1),
        ("strengthSpinBox", 1, 2000, 1),
        ("techLevelSpinBox", -1, 11, 1)
    ]


def get_spinbox_names() -> list:
    return [widget[0] for widget in get_spinbox_data()]


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_min_value(gui, widget_data):
    assert min_value_spinbox(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_max_value(gui, widget_data):
    assert max_value_spinbox(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_spinbox_data(), ids=get_spinbox_names())
def test_step_value(gui, widget_data):
    assert step_value_spinbox(gui, widget_data)


# ======================================================================================================================
# Check Box Tests
# ======================================================================================================================

def get_check_box_data() -> list:
    return [
        "cloakableCheckBox",
        "doubleOwnedCheckBox",
        "explodesCheckBox",
        "invisibleCheckBox",
        "selfHealingCheckBox",
        "sensorsCheckBox"
    ]


@pytest.mark.parametrize("widget_data", get_check_box_data())
def test_check_box_checked(gui, widget_data: str):
    assert check_box_checked(gui, widget_data)


@pytest.mark.parametrize("widget_data", get_check_box_data())
def test_check_box_unchecked(gui, widget_data: str):
    assert check_box_unchecked(gui, widget_data)


# ======================================================================================================================
# Combo Box Tests
# ======================================================================================================================

def verify_unit_selection(gui, item, _type):
    """
    Helper method to verify unit selection.

    :param gui: The gui instance.
    :param item: The item to select in the units field.
    :param _type: The unit type to select.
    :return: Does the field get assigned to the correct value.
    """
    index = gui.view.unitTypeComboBox.findText(_type)
    gui.view.unitTypeComboBox.setCurrentIndex(index)

    index = gui.view.unitComboBox.findText(item)
    gui.view.unitComboBox.setCurrentIndex(index)

    return gui.view.unitComboBox.currentText() == item


def get_unit_type_items() -> list:
    return ["Aircraft",
            "Ships",
            "Infantry",
            "Vehicles",
            "Buildings"]


@pytest.mark.parametrize("item", get_unit_type_items())
def test_type_selection_combo_box(gui, item):
    assert verify_combo_box_changes(gui, "unitTypeComboBox", item)


def get_aircraft() -> list:
    return [
        "Badger Bomber",
        "Chinook",
        "Hind Helicopter (Soviets)",
        "Longbow Helicopter (Allies)",
        "MIG",
        "Spy Plane",
        "Yak"
    ]


@pytest.mark.parametrize("item", get_aircraft())
def test_aircraft_units(gui, item):
    assert verify_unit_selection(gui, item, _type="Aircraft")


def get_buildings() -> list:
    return [
        "AA Gun",
        "AA SAM",
        "Airfield",
        "Allies Barracks",
        "Allies Tech Center",
        "Anti-Personnel Mine",
        "Anti-Vehicle Mine",
        "Barb Wire Fence",
        "Barrels",
        "Barrels2",
        "Camo Pill Box",
        "Chain Link Fence",
        "Command Center",
        "Concrete Wall",
        "Construction Yard",
        "Flame Turret",
        "Gap Generator",
        "Gun Turret",
        "Helipad",
        "Iron Curtain",
        "Kennel",
        "Missile Silo",
        "Paradox Device",
        "Pill Box",
        "Power Plant",
        "Power Plant - Advanced",
        "Radar Dome",
        "Refinery",
        "Sandbag Wall",
        "Service Depot",
        "Ship Yard",
        "Silo",
        "Soviet Barracks",
        "Soviet Tech Center",
        "Sub Pen",
        "Tesla Coil",
        "War Factory",
        "Wire Fence",
        "Wood Fence"
    ]


@pytest.mark.parametrize("item", get_buildings())
def test_buildings_units(gui, item):
    assert verify_unit_selection(gui, item, _type="Buildings")


def get_infantry() -> list:
    return [
        "Attack Dog",
        "Engineer",
        "Field Medic",
        "Flamethrower",
        "Grenadier",
        "Rifle Soldier",
        "Rocket Soldier",
        "Spy",
        "Tanya",
        "Thief"
    ]


@pytest.mark.parametrize("item", get_infantry())
def test_infantry_units(gui, item):
    assert verify_unit_selection(gui, item, _type="Infantry")


def get_ships() -> list:
    return [
        "Cruiser",
        "Destroyer",
        "Gun Boat",
        "Submarine",
        "Transport"
    ]


@pytest.mark.parametrize("item", get_ships())
def test_ship_units(gui, item):
    assert verify_unit_selection(gui, item, _type="Ships")


def get_vehicles() -> list:
    return [
        "APC",
        "Harvester",
        "Heavy Tank",
        "Light Tank",
        "MCV",
        "Mammoth Tank",
        "Medium Tank",
        "Mine Layer",
        "Mobile Artillery",
        "Mobile Gap Generator",
        "Mobile Radar Jammer",
        "Ranger Jeep",
        "V2 Rocket"
    ]


@pytest.mark.parametrize("item", get_vehicles())
def test_vehicles_units(gui, item):
    assert verify_unit_selection(gui, item, _type="Vehicles")

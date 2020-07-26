"""
Author:     David Walshe
Date:       26 July 2020
"""

# ======================================================================================================================
# SpinBox Tests
# ======================================================================================================================


def min_value_spinbox(form, widget_data: tuple):
    """
    WHEN: The spinbox widget is set to its minimum.
    THEN: Verify the widget is set to its minimum value.

    Helper method for obtaining the actual min value for a widget.

    :param form: The UI form under test.
    :param widget_data: The expected widget data.
    :return: The expected and actual min value for the widget.
    """
    MIN_VALUE = -1_000_000

    widget, expected_min, _, _ = widget_data

    form.view.__getattribute__(widget).setValue(MIN_VALUE)

    actual_min = form.view.__getattribute__(widget).value()

    return expected_min == actual_min


def max_value_spinbox(form, widget_data: tuple):
    """
    WHEN: The spinbox widget is set to its maximum.
    THEN: Verify the widget is set to its maximum value.

    Helper method for obtaining the actual max value for a widget.

    :param form: The UI form under test.
    :param widget_data: The expected widget data.
    :return: The expected and actual max value for the widget.
    """
    MAX_VALUE = 1_000_000

    widget, _, expected_max, _ = widget_data

    form.view.__getattribute__(widget).setValue(MAX_VALUE)

    actual_max = form.view.__getattribute__(widget).value()

    return expected_max == actual_max


def step_value_spinbox(form, widget_data: tuple):
    """
    WHEN: The spinbox widget is stepped.
    THEN: Verify the widget steps the correct amount.

    Helper method for obtaining the actual step value for a widget.

    :param form: The UI form under test.
    :param widget_data: The expected widget data.
    :return: The expected and actual step value for the widget.
    """
    MIN_VALUE = -1_000_000

    widget, _, _, expected_step = widget_data

    form.view.__getattribute__(widget).setValue(MIN_VALUE)

    initial_value = form.view.__getattribute__(widget).value()

    form.view.__getattribute__(widget).stepBy(1)

    end_value = form.view.__getattribute__(widget).value()

    actual_step = round(end_value - initial_value, 2)

    return expected_step == actual_step


# ======================================================================================================================
# Check Box Tests
# ======================================================================================================================


def check_box_unchecked(gui, widget_data: str):
    gui.view.__getattribute__(widget_data).setChecked(False)

    return gui.view.__getattribute__(widget_data).isChecked() is False


def check_box_checked(gui, widget_data: str):
    gui.view.__getattribute__(widget_data).setChecked(True)

    return gui.view.__getattribute__(widget_data).isChecked() is True


# ======================================================================================================================
# Combo Box Tests
# ======================================================================================================================

def verify_combo_box_changes(gui, widget_name: str, item):
    widget = gui.view.__getattribute__(widget_name)

    index = widget.findText(item)
    if index >= 0:
        widget.setCurrentIndex(index)

    print(f"{widget.currentText} {item}")

    return widget.currentText() == item

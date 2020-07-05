"""
Author:     David Walshe
Date:       04 July 2020
"""

from src.gui.view.view import View


class UnitStructureView(View):

    def c4_adjust_dependencies(self, c4_checkbox_state) -> None:
        """
        Updates Infiltrate field depending on state of C4 as there is a cross dependency.

        :param c4_checkbox_state: The state of the C4 checkbox
        """
        if c4_checkbox_state > 0:
            self.infiltrateCheckBox.setChecked(True)
            self.infiltrateCheckBox.setEnabled(False)
        else:
            self.infiltrateCheckBox.setEnabled(True)

    def disable_options(self) -> None:
        """
        Reset all options to disabled.
        """
        self.unitsGroupBox.setDisabled(True)
        self.infantryGroupBox.setDisabled(True)
        self.vehiclesGroupBox.setDisabled(True)
        self.structuresGroupBox.setDisabled(True)

    def enable_infantry_options(self) -> None:
        """
        Enable the infantry options section.
        """
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)
        self.infantryGroupBox.setEnabled(True)

    def enable_vehicles_options(self) -> None:
        """
        Enable the vehicles options section.
        """
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)
        self.vehiclesGroupBox.setEnabled(True)

    def enable_buildings_options(self) -> None:
        """
        Enable the building options section.
        """
        self.disable_options()
        self.structuresGroupBox.setEnabled(True)

    def enable_units_options(self) -> None:
        """
        Enable the unit options section.
        """
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)

    def update_options(self, state: str):
        """
        Selector for current valid options.

        :param state: The current option state to render.
        """
        state = state.lower()
        {
            "vehicles": self.enable_vehicles_options,
            "infantry": self.enable_infantry_options,
            "buildings": self.enable_buildings_options
        }.get(state, self.enable_units_options)()

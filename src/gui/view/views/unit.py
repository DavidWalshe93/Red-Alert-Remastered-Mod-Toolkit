"""
Author:     David Walshe
Date:       04 July 2020
"""

from src.gui.view.view import View


class UnitStructureView(View):

    def c4_adjust_dependencies(self, checkbox_state):
        print(checkbox_state)
        if checkbox_state > 0:
            self.infiltrateCheckBox.setChecked(True)
            self.infiltrateCheckBox.setEnabled(False)
        else:
            self.infiltrateCheckBox.setEnabled(True)

    def disable_options(self):
        self.unitsGroupBox.setDisabled(True)
        self.infantryGroupBox.setDisabled(True)
        self.vehiclesGroupBox.setDisabled(True)
        self.structuresGroupBox.setDisabled(True)

    def enable_infantry_options(self):
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)
        self.infantryGroupBox.setEnabled(True)

    def enable_vehicles_options(self):
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)
        self.vehiclesGroupBox.setEnabled(True)

    def enable_buildings_options(self):
        self.disable_options()
        self.structuresGroupBox.setEnabled(True)

    def enable_units_options(self):
        self.disable_options()
        self.unitsGroupBox.setEnabled(True)

    def update_options(self, state: str):
        state = state.lower()
        {
            "vehicles": self.enable_vehicles_options,
            "infantry": self.enable_infantry_options,
            "buildings": self.enable_buildings_options
        }.get(state, self.enable_units_options)()
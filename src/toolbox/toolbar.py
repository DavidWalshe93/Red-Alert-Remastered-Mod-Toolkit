"""
Author:     David Walshe
Date:       26 June 2020
"""


class Toolbar:

    def __init__(self):
        """
        Class constructor.
        """
        self.toolbar_y_location = 62
        self.toolbar_x_locations = {
            "map": 43,
            "smudge": 115,
            "overlay": 192,
            "terrain": 270,
            "infantry": 334,
            "unit_statistics": 400,
            "structures": 470,
            "resources": 565,
            "walls": 640,
            "waypoints": 724,
            "cell_triggers": 800
        }

    @property
    def map(self):
        return self.toolbar_x_locations["map"], self.toolbar_y_location

    @property
    def smudge(self):
        return self.toolbar_x_locations["smudge"], self.toolbar_y_location

    @property
    def overlay(self):
        return self.toolbar_x_locations["overlay"], self.toolbar_y_location

    @property
    def terrain(self):
        return self.toolbar_x_locations["terrain"], self.toolbar_y_location

    @property
    def infantry(self):
        return self.toolbar_x_locations["infantry"], self.toolbar_y_location

    @property
    def units(self):
        return self.toolbar_x_locations["unit_statistics"], self.toolbar_y_location

    @property
    def structures(self):
        return self.toolbar_x_locations["structures"], self.toolbar_y_location

    @property
    def resources(self):
        return self.toolbar_x_locations["resources"], self.toolbar_y_location

    @property
    def walls(self):
        return self.toolbar_x_locations["walls"], self.toolbar_y_location

    @property
    def waypoints(self):
        return self.toolbar_x_locations["waypoints"], self.toolbar_y_location

    @property
    def cell_triggers(self):
        return self.toolbar_x_locations["cell_triggers"], self.toolbar_y_location

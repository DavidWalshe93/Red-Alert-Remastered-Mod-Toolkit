"""
Author:     David Walshe
Date:       26 June 2020
"""

import pytest

from src.toolbox.toolbar import Toolbar


class TestToolbar:

    @pytest.fixture(autouse=True)
    def get_toolbar_resource(self):
        """
        Setup and Teardown.
        """
        self.toolbar = Toolbar()
        self.expected_y_location = 62
        self.expected_x_locations = {
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

        yield

        del self.toolbar

    @pytest.mark.parametrize("key", ("map", "smudge", "overlay", "terrain", "infantry", "unit_statistics",
                                     "structures", "resources", "walls", "waypoints", "cell_triggers")
                             )
    def test_toolbar_resources(self, key):
        """
        Verifies correct coordinate location for toolbar buttons.
        """
        assert (self.expected_x_locations[key], 62) == self.toolbar.__getattribute__(key)

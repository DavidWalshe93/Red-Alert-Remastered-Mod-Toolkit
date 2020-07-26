"""
Author:     David Walshe
Date:       26 July 2020
"""

import os
import pytest


@pytest.fixture
def gui():
    """
    Creates a Application instance to run tests against.

    :return: An application instance.
    """
    BASE_PROJECT_PATH = r"C:\Users\david\PycharmProjects\CNC_Map_Generator"
    os.environ["RA_USER_CONFIG_PATH"] = os.path.join(BASE_PROJECT_PATH, "user_config_test.json")
    os.environ["RA_DB_PATH"] = os.path.join(BASE_PROJECT_PATH, "db", "red_alert_data_test.db")
    os.environ["RA_LOGGER_CONFIG_PATH"] = os.path.join(BASE_PROJECT_PATH, "logger_config.yml")
    os.environ["RA_RESOURCE_PATH"] = os.path.join(BASE_PROJECT_PATH, "res", "raw")

    from src.controllers.app_controller import AppController
    gui = AppController()
    gui.setup()

    return gui

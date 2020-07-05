"""
Author:     David Walshe
Date:       25 June 2020
"""

# Setup environment variables for application.
import os

BASE_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

os.environ["RA_USER_CONFIG_PATH"] = os.path.join(BASE_PROJECT_PATH, "user_config.json")
os.environ["RA_DB_PATH"] = os.path.join(BASE_PROJECT_PATH, "db", "red_alert_data.db")
os.environ["RA_LOGGER_CONFIG_PATH"] = os.path.join(BASE_PROJECT_PATH, "logger_config.yml")


# Run application.
if __name__ == '__main__':
    # Setup logger, needs to be done here to enforce logger config in the rest of the application.
    import logging
    import src.logger.logger_setup

    from src.config.config_manager import ConfigManager
    from src.gui.gui import run

    # Register exit handlers.
    import atexit
    config_manager = ConfigManager()
    # config_manager.map_directory = "Hi There"

    atexit.register(config_manager.save_config)

    run()

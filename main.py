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
os.environ["RA_RESOURCE_PATH"] = os.path.join(BASE_PROJECT_PATH, "res", "raw")


def run():
    import logging
    from src.controllers.app_controller import AppController

    logger = logging.getLogger(__name__)

    logger.info(f"=" * 100)
    logger.info("Application launched")

    controller = AppController()
    controller.run()


# Run application.
if __name__ == '__main__':
    # Setup logger, needs to be done here to enforce logger config in the rest of the application.
    import src.logger.logger_setup

    from src.config.config_manager import ConfigManager

    # Register exit handlers.
    import atexit
    config_manager = ConfigManager()

    atexit.register(config_manager.save_config)

    run()

"""
Author:     David Walshe
Date:       25 June 2020
"""

# Setup environment variables for application.
import os
os.environ["RA_DB_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "red_alert_data.db")
os.environ["RA_LOGGER_CONFIG_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logger_config.yml")


# Run application.
if __name__ == '__main__':
    # Setup logger, needs to be done here to enforce logger config in the rest of the application.
    import logging
    import src.logger.logger_setup

    from src.gui.gui import run

    run()

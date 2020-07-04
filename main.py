"""
Author:     David Walshe
Date:       25 June 2020
"""

import os
os.environ["RA_DB_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "red_alert_data.db")
os.environ["RA_LOGGER_CONFIG_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logger_config.yml")


if __name__ == '__main__':
    from src.gui.gui import run

    run()

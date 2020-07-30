"""
Author:     David Walshe
Date:       28 July 2020
"""


import pyautogui as ui

from src.toolbox.asset_factory import AssetFactory


class MapDriver:

    def __init__(self, config_file: str):
        """
        Reads and creates a map based on a configuration file.
        """
        self.configuration = self.read_config(config_file)

    @staticmethod
    def read_config(config_file: str) -> dict:
        """
        Reads in a YAML config file.

        :return: The YAML config as a dict.
        """
        import yaml
        with open(config_file) as fh:
            return yaml.safe_load(fh)


if __name__ == '__main__':
    driver = MapDriver("sample.yml")
    print(driver.configuration)
    ui.alert("Press ok when the App Builder is in the foreground.")
    for item in driver.configuration:
        _id = list(item.keys())[0]

        asset = AssetFactory.get(_id)

        asset.draw(**item[_id])

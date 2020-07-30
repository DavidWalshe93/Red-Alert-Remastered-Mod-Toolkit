"""
Author:     David Walshe
Date:       28 July 2020
"""


from src.toolbox.assets.walls import Walls, BaseWalls
from src.toolbox.assets.resources import Resources
from src.toolbox.prebuilds.base import Base, WalledBase, FullBase


class AssetFactory:

    @staticmethod
    def get(_id, *args, **kwargs):
        asset = {
            "walls": AssetFactory.walls(*args, **kwargs),
            "base_walls": AssetFactory.base_walls(*args, **kwargs),
            "base": AssetFactory.base(*args, **kwargs),
            "walled_base": AssetFactory.walled_base(*args, **kwargs),
            "full_base": AssetFactory.full_base(*args, **kwargs),
            "resources": AssetFactory.walls(*args, **kwargs)
        }.get(_id, None)

        if asset is None:
            raise ValueError(f"'{_id}' declared in configuration file is not a valid asset.")

        return asset

    @staticmethod
    def walls(*args, **kwargs):
        return Walls(*args, **kwargs)

    @staticmethod
    def base_walls(*args, **kwargs):
        return BaseWalls(*args, **kwargs)

    @staticmethod
    def base(*args, **kwargs):
        return Base(*args, **kwargs)

    @staticmethod
    def walled_base(*args, **kwargs):
        return WalledBase(*args, **kwargs)

    @staticmethod
    def full_base(*args, **kwargs):
        return FullBase(*args, **kwargs)

    @staticmethod
    def resources(*args, **kwargs):
        return Resources(*args, **kwargs)
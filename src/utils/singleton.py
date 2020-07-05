"""
Author:     David Walshe
Date:       05 July 2020
"""


class Singleton(type):
    """
    Singleton design pattern used to limit possible database instances to one.
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        """
        Returns a new or existing class object depending on whether or not it was created previously.

        :return: The requested objects sole instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
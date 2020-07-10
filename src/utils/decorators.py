"""
Author:     David Walshe
Date:       09 July 2020
"""


def composed(*decos) -> callable:
    """
    Decorator composer, allows usage of multiple decorators on one method/function.

    :param decos: The decorators to bind.
    :return: A callable of all decorators bound.
    """
    def deco(f):
        for dec in reversed(decos):
            f = dec(f)
        return f
    return deco

"""
Author:     David Walshe
Date:       25 June 2020
"""


class Generator:

    def __init__(self):
        """
        Class constructor.
        """
        self.factions = ["Spain",
                         "Greece",
                         "USSR",
                         "England",
                         "Ukraine",
                         "Germany",
                         "France",
                         "Turkey",
                         "GoodGuy",
                         "BadGuy",
                         "Neutral",
                         "Special",
                         "Multi1",
                         "Multi2",
                         "Multi3",
                         "Multi4",
                         "Multi5",
                         "Multi6",
                         "Multi7",
                         "Multi8",
                         ]

    @property
    def faction_stubs(self):
        """

        :return:
        """
        faction_stubs = []

        for faction in self.factions:
            faction_stub = f"[{faction}]\n" \
                           f"Allies = {faction}\n" \
                           "MaxBuilding = 150\n" \
                           "MaxUnit = 150\n" \
                           "Edge = North\n" \
                           "Credits = 0\n\n"

            faction_stubs.append(faction_stub)

        return "".join(faction_stubs)


if __name__ == '__main__':
    gen = Generator()
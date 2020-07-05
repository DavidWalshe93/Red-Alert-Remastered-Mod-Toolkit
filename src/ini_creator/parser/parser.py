"""
Author:     David Walshe
Date:       05 July 2020
"""


from configparser import ConfigParser


class IniParser:

    def __init__(self):
        """
        Base class to parse ini files and return their extracted data.
        """
        self.config_parser = None
        self._data = []



    def get_section_data(self, section) -> dict:
        """
        For a passed section extract all options into a dict.

        :param section: The section to parse.
        :return: The extract options data.
        """
        data = {}

        options = self.config_parser.options(section)

        for option in options:
            try:
                data[option] = self.config_parser.get(section, option)
            except Exception as err:
                raise err

        return data

    def parse_file(self, file_path: str):
        """
        Read and parse the ini file passed.

        :param file_path: The file to read.
        """
        self._data = []
        self.config_parser = self.parser
        self.config_parser.read(file_path)

        for section in self.config_parser.sections():
            self._data.append(self.parse_data(section))

    @property
    def parser(self):
        config_parser = ConfigParser()
        config_parser.optionxform = str

        return config_parser

    def parse_data(self, section) -> dict:
        """
        How the data will be handled for a section.

        :param section: The current section being parsed.
        :return: The data being parsed.
        """
        data = self.get_section_data(section)
        data["Name"] = section
        data["Tag"] = section

        return data

    @property
    def data(self):
        return self._data


if __name__ == '__main__':
    parser = IniParser()
    parser.parse_file("./../../../res/raw/country_statistics.ini")
    print(parser.data)
    parser.parse_file("./../../../res/raw/unit_statistics/infantry.ini")
    print(parser.data)
    parser.parse_file("./../../../res/raw/unit_statistics/vehicles.ini")
    print(parser.data)
    parser.parse_file("./../../../res/raw/unit_statistics/ships.ini")
    print(parser.data)
    parser.parse_file("./../../../res/raw/unit_statistics/aircraft.ini")
    print(parser.data)
    parser.parse_file("./../../../res/raw/unit_statistics/buildings.ini")
    print(parser.data)



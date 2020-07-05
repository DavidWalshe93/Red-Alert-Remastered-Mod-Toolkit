"""
Author:     David Walshe
Date:       27 June 2020
"""

import json


class IniParser:

    def __init__(self):
        """
        Base super class for parsing INI file segments to extract the required information from them for reuse.
        """
        self.json_date = {}
        self.content = []
        self.unit_data = []

    def read_content(self, file_name: str):
        with open(f"../../res/raw/unit_statistics/{file_name}") as fh:
            self.content = fh.read().split("\n\n")

    @property
    def meta_data(self):
        try:
            name = self.unit_data[0].split(";")[1].strip()
            tag = self.unit_data[1]

            name = " ".join([word.capitalize() for word in name.split(" ")])
        except:
            # Name the same as the tag
            name = self.unit_data[0]
            tag = self.unit_data[0]

        return {
            "Name": name,
            "Tag": tag
        }

    @property
    def ini_data(self):
        # Get all data rows (rows that contain an =)
        unit = [data for data in self.unit_data if data.find("=") > -1]
        # Split ini data into key/value pairs.
        ini_data = {line.split("=")[0].strip(): line.split("=")[1].strip() for line in unit}
        # Remove stray comments in ini data
        ini_data = {key: value.split(";")[0].strip() for key, value in ini_data.items()}

        return ini_data

    def cast_numerics(self):
        casted_ini_data = self.ini_data

        for key, value in casted_ini_data.items():
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)

                casted_ini_data[key] = value
            except ValueError:
                pass

        return casted_ini_data

    def parse(self, file_name: str):
        self.read_content(file_name)

        json_data = []
        for i in range(1, len(self.content)):
            self.unit_data = self.content[i].split("\n")
            ini_date = self.cast_numerics()

            dt = {**self.meta_data, **ini_date}

            json_data.append(dt)

        return json_data


if __name__ == '__main__':
    parser = IniParser()
    print(parser.parse("aircraft.ini"))
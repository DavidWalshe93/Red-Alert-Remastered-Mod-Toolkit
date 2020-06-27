"""
Author:     David Walshe
Date:       27 June 2020
"""

import json
import pprint as pp


def defaults():
    return {
        "Ammo": -1,
        "Armor": "none",
        "Cloakable": "no",
        "Cost": 1,
        "Explodes": "no",
        "GuardRange": "DEFAULT",
        "Image": "DEFAULT",
        "Invisible": "no",
        "Owner": "allies,soviet",
        "Points": 0,
        "Prerequisite": "DEFAULT",
        "Primary": "none",
        "Secondary": "none",
        "ROT": 0,
        "Reload": 0,
        "SelfHealing": "no",
        "Sight": 1,
        "Strength": "DEFAULT",
        "TechLevel": -1,
        "Sensors": "no",
        "DoubleOwned": "no"
    }


def non_buildings():
    return {
        "Speed": 0,
        "Passengers": 0,
    }


def vehicles():
    return {
        **defaults(),
        **non_buildings(),
        "Crushable": "no",
        "Tracked": "no",
        "NoMovingFire": "no"
    }


def infantry():
    return {
        **defaults(),
        **non_buildings(),
        "C4": "no",
        "Fraidycat": "no",
        "Infiltrate": "no",
        "IsCanine": "no"
    }


def buildings():
    return {
        **defaults(),
        "BaseNormal": "yes",
        "Adjacent": "yes",
        "Bib": "no",
        "Capturable": "no",
        "Crewed": "no",
        "Power": 0,
        "Powered": "no",
        "Repairable": "yes",
        "Storage": 0,
        "Unsellable": "no",
        "WaterBound": "no"
    }


if __name__ == '__main__':

    with open("../../res/raw/unit_statistics/vehicles/soviets.ini") as fh:
        content = fh.read().split("\n\n")

    json_data = {}
    for i in range(1, len(content)):
        unit = content[i].split("\n")
        print(unit)
        meta = {
            "name": unit[0].split(";")[1].strip(),
            "tag": unit[1]
        }
        unit = [data for data in unit if data.find("=") > -1]
        dt = {line.split("=")[0].strip(): line.split("=")[1].strip() for line in unit}
        dt = {**defaults(), **meta, **dt}

        json_data.update({dt["name"]: dt})

    with open("../../res/units.json", "w") as fh:
        json.dump(json_data, fh, indent=4, sort_keys=True)

    # name = dt.pop("name")
    # tag = dt.pop("tag")
    # print(f"; {name}")
    # print(tag)
    # for key, value in dt.items():
    #     if value != "DEFAULT":
    #         print(f"{key}={value}")

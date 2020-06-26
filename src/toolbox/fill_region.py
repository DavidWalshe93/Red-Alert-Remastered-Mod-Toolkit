"""
Author:     David Walshe
Date:       25 June 2020
"""

import pyautogui as ui
import time





def fill_line(x_from, y_from, x_to, y_to):
    print("Here")
    ui.moveTo(x_map(x_from), y_map(y_from))
    print("Here")
    ui.keyDown("shift")
    for y in range(y_from, y_to):
        for x in range(x_from, x_to):
            ui.click(x_map(x), y_map(y))
            print(f"Working on {x}, {y} cell")
    ui.keyUp("shift")


if __name__ == '__main__':
    try:
        ui.alert("Press ok when ready to start")
        fill_line(0, 0, 10, 10)
    except ui.FailSafeException as err:
        print("Unsetting any key presses")
        ui.keyUp("shift")

    # while True:
    #     print(ui.position())
    #     time.sleep(0.1)
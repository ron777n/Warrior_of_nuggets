"""
The level
"""
import json

import pymunk

from Menus import EditorMenu
from physics.objects import Block, SlipperyBlock


def save(filename, player_location, blocks_data):
    save_json = dict()
    save_json["Player"] = list(player_location)
    save_json["Level"] = {}
    for location, data in blocks_data.items():
        save_json["Level"][str(location)] = data.json
    with open("Levels/Egg.lvl", "w") as file:
        json.dump(save_json, file)


def load(filename):
    canvas_data = {}
    with open(filename, "r") as file:
        loaded = json.load(file)

    player = tuple(loaded["Player"])
    # button_type = (pymunk.Body.DYNAMIC, (pymunk.Body.STATIC, pymunk.Body.DYNAMIC))
    # self.selected_block = (block, (), {"body_type": button_type})

    for location, data in loaded["Level"].items():
        if data[0] == "Block":
            block = Block
        elif data[0] == "SlipperyBlock":
            block = SlipperyBlock
        else:
            block = Block

        for block_data_type, value in data[2].items():
            if block_data_type == "body_type":
                data[2][block_data_type] = (value, (pymunk.Body.STATIC, pymunk.Body.DYNAMIC))
            else:
                print(block_data_type, value)
        location: str
        comma = location.find(",")

        canvas_data[(int(location[1:comma]), int(location[comma + 2:-1]))] = \
            EditorMenu.EditorTile((block, data[1], data[2]))

    return player, canvas_data

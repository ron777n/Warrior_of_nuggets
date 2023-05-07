"""
The level
"""
import itertools
import json
import os

import pymunk

from Menus import EditorMenu
from physics.objects import Block, SlipperyBlock
from settings import TILE_SIZE


def save(filename, blocks_data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    save_json = {}
    for location, data in blocks_data.items():
        if isinstance(data, EditorMenu.EditorTile):
            save_json[str(location)] = data.json
        else:
            save_json[str(location)] = data

    with open(filename, "w") as file:
        json.dump(save_json, file)


def load(filename, scale=False) -> dict:
    if not os.path.isfile(filename):
        return {(0, 0): "player"}
    with open(filename, "r") as file:
        loaded = json.load(file)

    canvas_data = {}

    for location, data in loaded.items():
        location: str
        comma = location.find(",")
        location_tuple = (int(location[1:comma]), int(location[comma + 2:-1]))
        if isinstance(data, str):
            canvas_data[location_tuple] = "player"
            continue
        if data[0] == "Block":
            block = Block
        elif data[0] == "SlipperyBlock":
            block = SlipperyBlock
        else:
            block = Block

        params: tuple = data[1]

        kwargs = {}

        for key, (value, possible_values) in data[2].items():
            kwargs[key] = (value, possible_values)

        if scale:
            location_tuple = location_tuple[0] * TILE_SIZE, location_tuple[1] * TILE_SIZE

        canvas_data[location_tuple] = \
            EditorMenu.EditorTile((block, params, kwargs))

    return canvas_data

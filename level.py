"""
The level
"""
import json
import os

import pygame

from Utils.Gui.Menus import EditorMenu
from physics.objects import block_shape
from settings import TILE_SIZE


def save(filename, blocks_data, buttons_data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    blocks_json = {}
    for location, data in blocks_data.items():
        if isinstance(data, EditorMenu.EditorTile):
            blocks_json[str(location)] = data.json
        else:
            blocks_json[str(location)] = data
    save_json = {"Level": blocks_json, "Editor": buttons_data}

    with open(filename, "w") as file:
        json.dump(save_json, file, indent=2)


def load(filename, editor=False) -> dict:
    if not os.path.isfile(filename):
        if editor:
            return {"Level": {(0, 0): "player"}, "Editor": []}
        return {(0, 0): "player"}
    with open(filename, "r") as file:
        loaded = json.load(file)

    canvas_data = {}

    for location, data in loaded["Level"].items():
        location: str
        comma = location.find(",")
        location_tuple = (int(location[1:comma]), int(location[comma + 2:-1]))
        if not editor:
            location_tuple = location_tuple[0] * TILE_SIZE, location_tuple[1] * TILE_SIZE

        if isinstance(data, str):
            canvas_data[location_tuple] = "player"
            continue
        if data[0] == "block_shape":
            shape = block_shape
        else:
            continue

        params: tuple = data[1]

        kwargs = {}

        for key, (value, possible_values) in data[2].items():
            kwargs[key] = (value, possible_values)
            if key == "image":
                kwargs["image"] = (pygame.image.load(value), value), possible_values

        canvas_data[location_tuple] = \
            EditorMenu.EditorTile((shape, params, kwargs))

    if editor:
        editor_data = []
        for shape, data in loaded["Editor"]:
            shape_data = {}
            for key, val in data.items():
                if key == "image":
                    val = ((pygame.image.load(val[0]), val[0]), val[1])
                shape_data[key] = val
            editor_data.append((shape, shape_data))
        canvas_data = {"Level": canvas_data, "Editor": editor_data}

    return canvas_data

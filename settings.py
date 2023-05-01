"""
handles the settings
"""
import json

import pygame

with open("settings.json") as f:
    settings = json.load(f)

SCREEN_WIDTH = settings["Screen"]["Size"][0]
SCREEN_HEIGHT = settings["Screen"]["Size"][1]

TILE_SIZE = settings["Editor"]["TileSize"]

PLAYER_HEAD = pygame.image.load(settings["Player"]["Head"])

__all__ = ["settings", "SCREEN_WIDTH", "SCREEN_HEIGHT", "TILE_SIZE", "PLAYER_HEAD"]

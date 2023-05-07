"""
yes
"""
from typing import Optional, Union

import pygame
import pymunk
from pymunk import pygame_util

import level
from Menus.EditorMenu import EditorTile
from player import Player
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE
from Utils.camera import Camera


class Game:
    """
    pass
    """
    def __init__(self, transition, level_name):
        self.transition = transition
        self.level_name = level_name

        self.display_surface = pygame.display.get_surface()

        self.space = pymunk.Space()
        self.space.gravity = (0, 10)

        self.camera = Camera(("static", pygame.image.load("sprites/temp/background.jpg")),
                             (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player: Optional[Player] = None
        self.debug_options = pymunk.pygame_util.DrawOptions(self.display_surface)

    def reset(self):
        self.camera.clear(self.space)
        data = level.load(self.level_name, False)
        self.add_objects(data)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            self.handle_event(event)

    def run(self, dt):
        self.event_loop()
        self.player.update()
        self.camera.update()
        self.camera.display()
        self.space.step(dt)

    def add_objects(self, data):
        tile: EditorTile
        player = False
        for location, tile in data.items():
            rect = pygame.Rect((location[0], location[1]), (TILE_SIZE, TILE_SIZE))
            if isinstance(tile, str):
                if tile == "player":
                    self.player: Player = Player(self.space, location, camera=self.camera)
                    player = True
                    self.camera.append(self.player)
                continue
            self.camera.append(
                tile.main_block[0](
                    self.space, rect,
                    *tile.main_block[1], **{name: val for name, (val, _, _) in tile.main_block[2].items()}
                )
            )
        if not player:
            raise ValueError("Player location not found in level")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.transition()
            elif event.key == pygame.K_EQUALS:
                self.camera.zoom(2)
            elif event.key == pygame.K_MINUS:
                self.camera.zoom(0.5)
        self.player.handle_event(event)

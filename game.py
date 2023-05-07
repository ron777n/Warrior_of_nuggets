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
        data = level.load(level_name, True)

        self.space = pymunk.Space()
        self.space.gravity = (0, 10)

        self.camera = Camera(("static", pygame.image.load("sprites/temp/background.jpg")),
                             (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player: Optional[Player] = None
        self.debug_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        self.add_objects(data)

    def reset(self):
        if self.player is None:
            return
        self.camera.clear(self.space)
        data = level.load(self.level_name, True)
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
        for location, tile in data.items():
            self.add_object(location, tile)

    def add_object(self, location, data: Union[EditorTile, str]):
        rect = pygame.Rect((location[0], location[1]), (TILE_SIZE, TILE_SIZE))
        if isinstance(data, str):
            if data == "player":
                self.player: Player = Player(self.space, location, camera=self.camera)
                self.camera.append(self.player)
            return
        self.camera.append(
            data.main_block[0](
                self.space, rect,
                *data.main_block[1], **{name: val for name, (val, _, _) in data.main_block[2].items()}
                )
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.transition()
            elif event.key == pygame.K_EQUALS:
                self.camera.zoom(2)
            elif event.key == pygame.K_MINUS:
                self.camera.zoom(0.5)
        self.player.handle_event(event)

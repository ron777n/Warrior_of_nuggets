"""
yes
"""
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
        player_spawn, data = level.load(level_name, True)

        self.space = pymunk.Space()
        self.space.gravity = (0, 10)

        self.camera = Camera(pygame.image.load("sprites/temp/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player: Player = Player(self.space, player_spawn, camera=self.camera)
        self.camera.append(self.player)
        self.debug_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        self.add_objects(data)

    def reset(self):
        self.camera.clear(self.space)
        player_spawn, data = level.load(self.level_name, True)
        self.player: Player = Player(self.space, player_spawn, camera=self.camera)
        self.camera.append(self.player)

        self.add_objects(data)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            self.handle_event(event)

    def run(self, dt):
        self.event_loop()
        self.camera.display()
        self.camera.update()
        self.player.update()
        self.space.step(dt)

    def add_objects(self, data):
        tile: EditorTile
        for location, tile in data.items():
            self.add_object(location, tile)

    def add_object(self, location, data: EditorTile):
        rect = pygame.Rect((location[0], location[1]), (TILE_SIZE, TILE_SIZE))
        self.camera.append(
            data.main_block[0](
                self.space, rect,
                *data.main_block[1], **{name: val for name, (val, _) in data.main_block[2].items()}
                )
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.transition()
        self.player.handle_event(event)

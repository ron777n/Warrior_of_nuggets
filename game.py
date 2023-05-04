"""
yes
"""
import pygame
import pymunk
from pymunk import pygame_util

import level
from Menus.EditorMenu import EditorTile
from player import Player
from settings import TILE_SIZE


class Game:
    """
    pass
    """
    def __init__(self, level_name):
        self.display_surface = pygame.display.get_surface()
        self.camera = []
        player_spawn, data = level.load(level_name, True)

        self.space = pymunk.Space()
        self.space.gravity = (0, 10)

        self.player: Player = Player(self.space, player_spawn)
        self.camera.append(self.player)
        self.debug_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        self.add_objects(data)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            self.player.handle_event(event)

    def run(self, dt):
        self.event_loop()
        self.draw()
        self.player.update()
        # self.space.debug_draw(self.debug_options)
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

    def draw(self):
        self.display_surface.fill("white")
        for block in self.camera:
            self.display_surface.blit(block.image, block.rect)

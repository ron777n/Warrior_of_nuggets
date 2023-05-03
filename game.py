"""
yes
"""
import pygame
import pymunk

import level
from Menus.EditorMenu import EditorTile
from settings import TILE_SIZE


class Game:
    """
    pass
    """
    def __init__(self, level_name):
        self.display_surface = pygame.display.get_surface()
        self.camera = []

        self.space = pymunk.Space()
        self.space.gravity = (0, 10)

        player_spawn, data = level.load(level_name)
        self.add_objects(data)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

    def run(self, dt):
        self.event_loop()
        self.draw()
        self.space.step(dt)

    def add_objects(self, data):
        tile: EditorTile
        for location, tile in data.items():
            self.add_object(location, tile)

    def add_object(self, location, data: EditorTile):
        rect = pygame.Rect((location[0] * TILE_SIZE, location[1] * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
        self.camera.append(
            data.main_block[0](
                self.space, rect,
                *data.main_block[1], **{name: val for name, (val, _) in data.main_block[2].items()}
                )
        )

    def draw(self):
        self.display_surface.fill("white")
        for block in self.camera:
            # print(block.position)
            self.display_surface.blit(block.image, block.rect)

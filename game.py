"""
yes
"""
from typing import Optional

import pygame
import pymunk
from pymunk import pygame_util

import level
from my_events import PLAYER_DIED_EVENT
from physics.objects import Solid
from Utils.Gui.Menus.EditorMenu import EditorTile
from Player import Player
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
        self.camera.update(dt)
        self.camera.display()
        # self.space.debug_draw(self.debug_options)
        self.display_menus()
        self.space.step(dt)

    def add_objects(self, data):
        tile: EditorTile
        player = False
        for location, tile in data.items():
            if isinstance(tile, str):
                if tile == "player":
                    self.player: Player = Player(self.space, location, camera=self.camera)
                    player = True
                continue
            values = tile.main_block[2]
            shape = tile.main_block[0](
                    None, (TILE_SIZE, TILE_SIZE),
                    *tile.main_block[1], **{name: val for name, (val, _, _) in
                                            values.items() if name not in ("body_type", "image")}
                )

            body = Solid(self.space, location, shape,
                         body_type_name=values["body_type"][0], image_path=values["image"][0][1])
            self.camera.append(
                body
            )
        if not player:
            raise ValueError("Player location not found in level")

    def handle_event(self, event):
        if event.type == PLAYER_DIED_EVENT:
            raise KeyboardInterrupt()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.transition()
            elif event.key == pygame.K_EQUALS:
                self.camera.zoom(2)
            elif event.key == pygame.K_MINUS:
                self.camera.zoom(0.5)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.player.inventory_active:
                if self.player.inventory.click(event.pos, event.button, True):
                    return
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.player.inventory_active:
                if self.player.inventory.click(event.pos, event.button, False):
                    return
        self.player.handle_event(event)

    def display_menus(self):
        if self.player.inventory_active:
            self.player.inventory.display(self.display_surface)

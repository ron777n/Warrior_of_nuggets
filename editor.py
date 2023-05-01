"""
This is for the level creator.
"""
import itertools

import pygame
import pymunk
from pygame.math import Vector2
import json

import Utils.Gui as Gui
from Menus import EditorMenu
from physics.objects import Block, SlipperyBlock, Solid
from settings import *

with open("settings.json") as f:
    settings = json.load(f)


class Editor:
    """
    The class that holds the loop
    """

    def __init__(self, ):
        self.active_blocks = []
        self.selected_block = None
        self.display_surface = pygame.display.get_surface()
        self.origin = Vector2()
        self.canvas_data: dict[tuple[int, int], EditorMenu.EditorTile] = {}
        self.space = pymunk.Space()
        self.space.gravity = (0, 10)
        self.settings = EditorMenu.TileMenu()
        self.player = (0, 0)

        # self.selection_index = 0

        self.testing = False
        self.menu = EditorMenu.EditorMenu(
            (
                self.set_block,
                self.set_player,
                self.delete_block
            ),
            Block, SlipperyBlock
        )

    def delete_block(self):
        self.selected_block = "delete"

    def set_player(self):
        self.selected_block = "player"

    def set_block(self, block):
        self.selected_block = [block, (),
                               {"body_type": (pymunk.Body.DYNAMIC,
                                              itertools.cycle((pymunk.Body.STATIC, pymunk.Body.DYNAMIC)))}]

    def event_loop(self, delta_time):
        """
        handles the Game loop
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            self.handle_event(event)

    def handle_event(self, event: pygame.event):
        """
        handles the event, because
        :param event:
        """
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[1] or \
                    (event.buttons[0] and pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.origin += Vector2(event.rel)
            elif event.buttons[0]:
                self.click(event.pos, 1, True)

        elif event.type == pygame.MOUSEWHEEL:
            if event.x:
                self.origin.x -= event.x * TILE_SIZE / 2
            if event.y:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.origin.x -= event.y * TILE_SIZE / 2
                else:
                    self.origin.y -= event.y * TILE_SIZE / 2

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_data = event.pos, event.button, True
            if self.settings.active:
                if not self.settings.click(*mouse_data):
                    self.click(*mouse_data)
            elif not self.menu.click(*mouse_data):
                self.click(*mouse_data)

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_data = event.pos, event.button, False
            if self.settings.active:
                self.settings.click(*mouse_data)
            else:
                self.menu.click(*mouse_data)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not self.testing:
                    self.testing = True
                    self.spawn_blocks()
                else:
                    self.testing = False
                    self.clear()
                    # self.space.remove()

    def draw_tile_lines(self):
        """
        draws the tiles(grid)
        """
        cols, rows = settings["Screen"]["Size"]

        rows //= settings["Editor"]["TileSize"]
        cols //= settings["Editor"]["TileSize"]

        for col in range(cols + 1):
            x = self.origin.x + col * settings["Editor"]["TileSize"]
            x %= settings["Screen"]["Size"][0]
            pygame.draw.line(self.display_surface, settings["Editor"]["GridColor"],
                             (x, 0), (x, settings["Screen"]["Size"][1]))

        for row in range(rows + 1):
            y = self.origin.y + row * settings["Editor"]["TileSize"]
            y %= settings["Screen"]["Size"][1]
            pygame.draw.line(self.display_surface, settings["Editor"]["GridColor"],
                             (0, y), (settings["Screen"]["Size"][0], y))

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        if not down:
            return False
        tile_cords = int((location[0] - self.origin[0]) // TILE_SIZE), int((location[1] - self.origin[1]) // TILE_SIZE)

        if tile_cords not in self.canvas_data:
            if button_type != pygame.BUTTON_LEFT:
                return False
            if isinstance(self.selected_block, list):
                self.canvas_data[tile_cords] = EditorMenu.EditorTile(self.selected_block)
            elif self.selected_block == "player":
                self.player = tile_cords
        elif self.selected_block == "delete" and button_type == pygame.BUTTON_LEFT:
            del self.canvas_data[tile_cords]

        elif button_type == pygame.BUTTON_RIGHT:
            tile = self.canvas_data[tile_cords]
            if self.settings and self.settings.current == tile:
                self.settings.active = False
            else:
                self.settings.reset(tile)

        return True

    def run(self, dt):
        """
        starts the game loop
        """
        self.display_surface.fill("white")
        self.event_loop(dt)
        self.draw_tile_lines()
        self.draw_blocks()
        self.draw_player()

        # self.display_surface.blit()
        if self.settings.active:
            self.settings.display(self.display_surface)
        else:
            self.menu.display(self.display_surface)
        self.space.step(dt if self.testing else 0)

    def draw_blocks(self):
        if self.testing:
            for block in self.active_blocks:
                self.display_surface.blit(block.image, block.rect)
            return
        for coordinate, tile in self.canvas_data.items():
            rect = pygame.rect.Rect(coordinate[0] * 64 + self.origin[0],
                                    coordinate[1] * 64 + self.origin[1],
                                    TILE_SIZE, TILE_SIZE)
            self.display_surface.blit(
                pygame.transform.scale(tile.image, (TILE_SIZE, TILE_SIZE)), rect)

    def spawn_blocks(self):
        for coordinate, tile in self.canvas_data.items():
            rect = pygame.rect.Rect(coordinate[0] * 64 + self.origin[0],
                                    coordinate[1] * 64 + self.origin[1],
                                    TILE_SIZE, TILE_SIZE)
            block = tile.main_block[0](self.space, rect, *tile.main_block[1],
                                       **{name: val for name, (val, _) in tile.main_block[2].items()})
            self.active_blocks.append(block)

    def clear(self):
        for block in self.active_blocks:
            self.space.remove(block, block.shape)
        self.active_blocks.clear()

    def draw_player(self):
        rect = PLAYER_HEAD.get_rect().move(
            self.player[0] * 64 + self.origin[0], self.player[1] * 64 + self.origin[1])
        self.display_surface.blit(pygame.transform.scale(PLAYER_HEAD, (64, 64)), rect)

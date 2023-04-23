"""
This is for the level creator.
"""
import pygame
from pygame.math import Vector2
import json

import Utils.Gui as Gui
from Menus import EditorMenu
from settings import *

with open("settings.json") as f:
    settings = json.load(f)


class Editor:
    """
    The class that holds the loop
    """

    def __init__(self, ):
        self.display_surface = pygame.display.get_surface()
        self.origin = Vector2()
        self.canvas_data: dict[tuple[int, int], any] = {}

        self.selection_index = 0

        self.menu = EditorMenu.Menu()

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
            if self.menu.click(*mouse_data):
                return
            self.click(*mouse_data)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.menu.click(event.pos, event.button, False)

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_d, pygame.K_a):
                self.selection_index = min(
                    max(
                        self.selection_index + (1 if event.key in (pygame.K_d, pygame.K_RIGHT) else -1),
                        0),
                    18)
                print(self.selection_index)

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

    def run(self, dt):
        """
        starts the game loop
        """
        self.display_surface.fill("white")
        self.event_loop(dt)
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, "black", self.origin, 10)
        self.menu.display()

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        if button_type != pygame.BUTTON_LEFT:
            return False
        tile_cords = int((location[0] - self.origin[0]) // TILE_SIZE), int((location[1] - self.origin[1]) // TILE_SIZE)

        if tile_cords not in self.canvas_data:
            self.canvas_data[tile_cords] = EditorTile()
            print("planted", "egg", tile_cords)
        else:
            print("found", self.canvas_data[tile_cords], tile_cords)

        return True


class EditorTile:
    """
    The editor tile, handles what's in the specific tile
    """

    def __init__(self):
        main_block = None

        additions = []

"""
This is for the level creator.
"""
import pygame
from pygame.math import Vector2
import json

import Utils.Gui as Gui

with open("settings.json") as f:
    settings = json.load(f)


class Editor:
    """
    The class that holds the loop
    """
    def __init__(self, ):
        self.display_surface = pygame.display.get_surface()
        self.origin = Vector2()
        self.gui: list[Gui.BaseGui] = []
        self.create_buttons()

    def create_buttons(self):
        a = Gui.BaseGui()
        self.gui.append(a)

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
                self.origin.x -= event.x * 64 / 2
            if event.y:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.origin.x -= event.y * 64 / 2
                else:
                    self.origin.y -= event.y * 50

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.gui:
                button.click((event.pos, (event.button, 1)))

        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.gui:
                button.click((event.pos, (event.button, 0)))

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

    def load_interface(self):
        button: Gui.BaseGui
        for button in self.gui:
            self.display_surface.blit(button.image, button.rect)

    def run(self, dt):
        """
        starts the game loop
        """
        self.display_surface.fill("white")
        self.event_loop(dt)
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, "black", self.origin, 10)
        self.load_interface()

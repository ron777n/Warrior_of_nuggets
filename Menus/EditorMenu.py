"""
The menu for the editor
"""
import typing
from collections.abc import Iterable

import pygame.display
import pymunk

from physics.objects import Solid, BaseObject
from settings import *
from Utils import Gui

margin = 6
width = 180
height = SCREEN_HEIGHT - margin


class EditorMenu(Gui.Menu):
    """
    The menu class for the editor
    """

    def __init__(self, set_function: callable, *classes: type[BaseObject]):
        self.selected_block = None
        self.rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.buttons: list[Gui.BaseGui] = []

        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect = pygame.Rect(top_left, (width, height))

        self.create_buttons(set_function, *classes)

    def create_buttons(self, set_class, *classes):
        """
        just creates all the buttons
        """
        # menu area
        columns = 2

        # button areas
        button_margin = 5

        box_size = width / (columns + 1)
        for i, class_type in enumerate(classes, start=1):
            rect = pygame.rect.Rect(
                self.rect.left + box_size * (i % columns),
                self.rect.top + box_size * ((i - 1) // columns),
                box_size,
                box_size)
            button_1 = Gui.Button(rect.inflate(-button_margin, -button_margin),
                                  lambda save=class_type: set_class(save), image=class_type.base_image)
            self.buttons.append(button_1)

    def display(self, display_surface):
        """
        puts everything on the screen
        """
        for button in self.buttons:
            display_surface.blit(button.image, button.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        clicks all the inputs on the menu
        """
        r = False
        for button in self.buttons:
            if button.click(location, button_type, down):
                r = True
        return r


class EditorTile:
    """
    The editor tile, handles what's in the specific tile
    """

    def __init__(self, selection):
        self.main_block: tuple[type[Solid], tuple, dict[any, tuple[any, generator]]] = selection
        self.main_block = (*self.main_block[:2], self.main_block[2].copy())

        additions = []

    @property
    def image(self) -> pygame.surface.Surface:
        return self.main_block[0].base_image


class TileMenu(Gui.Menu):
    def __init__(self):
        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect = pygame.Rect(top_left, (width, height))
        self.buttons = {}
        self.active = False
        self.current = None

    def reset(self, tile: EditorTile):
        self.active = True
        self.current = tile
        self.buttons.clear()
        columns = 1
        # button areas
        button_margin = 5

        box_size = width / (columns + 1)
        for i, (name, (value, possible_values)) in \
                enumerate(tile.main_block[2].items(), start=1):
            print(name, value, possible_values, type(possible_values))
            func: callable = lambda: 0
            if isinstance(possible_values, Iterable):
                def func():
                    a = next(possible_values)
                    print(a)
                    tile.main_block[2][name] = (a, possible_values)

            rect = pygame.rect.Rect(
                self.rect.left + box_size * (i % columns),
                self.rect.top + box_size * ((i - 1) // columns),
                box_size,
                box_size)
            button_1 = Gui.Button(
                rect.inflate(-button_margin, -button_margin),
                func
            )
            self.buttons[button_1] = tile

    def display(self, display_surface: pygame.surface.SurfaceType):
        for button, val in self.buttons.items():
            display_surface.blit(button.image, button.rect)
            img = pygame.surface.Surface(button.rect.size)
            img.fill("red")
            display_surface.blit(img, button.rect.move((width // 2, 0)))

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = False
        for button in self.buttons:
            r = r or button.click(location, button_type, down)
        return r

"""
The menu for the editor
"""
import itertools
import typing
from collections.abc import Iterable

import pygame.display
import pymunk

from physics.objects import Solid, BaseObject
from settings import *
from Utils import Gui, image_utils

margin = 0
width = 192
height = SCREEN_HEIGHT - margin


class EditorMenu(Gui.Menu):
    """
    The menu class for the editor
    """

    def __init__(self, set_functions: tuple[callable, ...], *classes: type[BaseObject]):
        self.selected_block = None
        self.rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.buttons: list[Gui.BaseGui] = []
        self.buttons_i = 1

        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect = pygame.Rect(top_left, (width, height))

        self.button_margin = 5
        self.columns = 2
        self.box_size = width / (self.columns + 1)

        self.create_buttons(set_functions, *classes)

    def add_button(self, func: (callable, Iterable, dict), img):
        rect = pygame.rect.Rect(
            self.rect.left + self.box_size * (self.buttons_i % self.columns),
            self.rect.top + self.box_size * ((self.buttons_i - 1) // self.columns),
            self.box_size,
            self.box_size)
        button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin),
                              lambda: func[0](*func[1], **func[2]), image=img)
        self.buttons.append(button_1)
        self.buttons_i += 1

    def create_buttons(self, functions, *classes):
        """
        just creates all the buttons
        """
        create_block = functions[0]
        set_player = functions[1]
        delete_block = functions[2]

        self.add_button((set_player, (), {}), PLAYER_HEAD)
        red = pygame.Surface((64, 64))
        red.fill("red")
        self.add_button((delete_block, (), {}), red)

        for i, class_type in enumerate(classes, start=3):
            self.add_button((create_block, (class_type,), {}), class_type.base_image)

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
        r = self.rect.collidepoint(location)
        for button in self.buttons:
            r = button.click(location, button_type, down) or r
        return r


class EditorTile:
    """
    The editor tile, handles what's in the specific tile
    """

    def __init__(self, selection: tuple[type(Solid), tuple, dict[any, tuple[any, tuple]]]):
        self.main_block: tuple[type(Solid), tuple, dict[any, list[any, Iterable]]] = \
            (selection[0], selection[1], {a: [b[0], itertools.cycle(b[1])] for a, b in selection[2].items()})
        self.main_block = (*self.main_block[:2], self.main_block[2].copy())

        additions = []

    @property
    def json(self):
        return {self.main_block[0].__name__: (list(self.main_block[1]),
                                              {name: values[0] for name, values in self.main_block[2].items()})}

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
            # print(name, value, possible_values, type(possible_values))
            func: callable = lambda: 0
            if isinstance(possible_values, Iterable):
                def func():
                    a = next(possible_values)
                    tile.main_block[2][name][:] = [a, possible_values]

            rect = pygame.rect.Rect(
                self.rect.left + box_size * (i % columns),
                self.rect.top + box_size * ((i - 1) // columns),
                box_size,
                box_size)
            button_1 = Gui.Button(
                rect.inflate(-button_margin, -button_margin),
                func
            )
            self.buttons[button_1] = tile.main_block[2][name]

    def display(self, display_surface: pygame.surface.Surface):
        for button, value in self.buttons.items():
            display_surface.blit(button.image, button.rect)
            img = pygame.surface.Surface(button.rect.size)
            # print((button, value))
            img.fill("red")
            rect = img.get_rect().copy()
            text = image_utils.Text(str(value[0])).wrap(rect.size)

            img.blit(text, rect)
            display_surface.blit(img, button.rect.move((width // 2, 0)))

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
        for button in self.buttons:
            r = button.click(location, button_type, down) or r
        return r

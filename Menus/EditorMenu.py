"""
The menu for the editor
"""
import itertools
import typing
from collections.abc import Iterable

import pygame.display
import pymunk

from Utils.image_utils import Text
from physics.objects import Solid, BaseObject
from settings import *
from Utils import Gui, image_utils

margin = 0
width = 192
width1 = 128
height = SCREEN_HEIGHT - margin
height1 = 128


class EditorMenu(Gui.Menu):
    """
    The menu class for the editor
    """

    def __init__(self, set_functions: tuple[callable, ...], *classes: type[BaseObject]):
        self.selected_block = None
        self.buttons: list[Gui.BaseGui] = []
        self.buttons_i = 0
        self.object_i = 1

        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.scroll_rect = pygame.Rect(top_left, (width, height))
        top_left_1 = (SCREEN_WIDTH - width - margin - width1, 0)
        self.button_rect = pygame.Rect(top_left_1, (width1, height1))

        self.button_margin = 5
        self.columns = 3
        self.columns1 = 2
        self.box_size = width / self.columns
        self.background = pygame.transform.scale(pygame.image.load("sprites/Gui/BlocksMenu.png"), self.scroll_rect.size)
        self.background1 = pygame.transform.scale(pygame.image.load("sprites/Gui/BlocksMenu.png"), self.button_rect.size)

        self.create_block = set_functions[0]
        self.set_player = set_functions[1]
        self.delete_block = set_functions[2]
        self.start_button = set_functions[3]
        self.save_level = set_functions[4]

        self.create_buttons(classes)

    def add_button(self, class_type, values, img):
        rect = pygame.rect.Rect(
            self.scroll_rect.left + self.box_size * (self.buttons_i % self.columns),
            self.scroll_rect.top + self.box_size * (self.buttons_i // self.columns),
            self.box_size,
            self.box_size)
        button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin),
                              lambda: self.create_block(class_type, values), image=img)
        self.buttons.append(button_1)
        self.buttons_i += 1

    def add_object(self, func: (callable, Iterable, dict), text):
        rect = pygame.rect.Rect(
            self.button_rect.left + self.box_size * (self.object_i % self.columns1),
            self.button_rect.top + self.box_size * ((self.object_i - 1) // self.columns1),
            self.box_size,
            self.box_size)
        base_image = pygame.image.load("sprites/Gui/Button.png")
        set_image = pygame.transform.scale(base_image, rect.size)
        player_text = Text(text, (255, 0, 0))
        set_image.blit(player_text, (rect.width/player_text.size[0], player_text.size[1]/2))
        button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin),
                              lambda: func[0](*func[1], **func[2]), image=set_image)
        self.buttons.append(button_1)
        self.object_i += 1

    def create_buttons(self, classes):
        """
        just creates all the buttons
        """
        self.add_object((self.set_player, (), {}), "player")

        self.add_object((self.delete_block, (), {}), "delete")

        self.add_object((self.start_button, (), {},),  "start")

        self.add_object((self.save_level, (), {},), "save")

        for i, class_type in enumerate(classes, start=1):
            self.add_button(class_type, {}, class_type.base_image)

    def display(self, display_surface):
        """
        puts everything on the screen
        """
        display_surface.blit(self.background, self.scroll_rect)
        display_surface.blit(self.background1, self.button_rect)

        for button in self.buttons:
            display_surface.blit(button.image, button.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        clicks all the inputs on the menu
        """
        r = self.collide_point(location)
        for button in self.buttons:
            r = button.click(location, button_type, down) or r
        return r

    def collide_point(self, point):
        return self.scroll_rect.collidepoint(point) or self.button_rect.collidepoint(point)


class EditorTile:
    """
    The editor tile, handles what's in the specific tile
    """

    def __init__(self, selection: tuple[type(Solid), tuple, dict[any, tuple[any, tuple]]]):
        block_data = {}
        for key, (value, possible_values) in selection[2].items():
            data_swap = None
            if typing.get_origin(possible_values) == typing.Literal:
                possible_values = typing.get_args(possible_values)
            if isinstance(possible_values, Iterable):
                data_swap = itertools.cycle(possible_values)
                for val in data_swap:
                    if val == value:
                        break
            if data_swap is not None:
                block_data[key] = [value, possible_values, data_swap]
        self.main_block: tuple[type(Solid), tuple, dict[any, list[any, any, any]]] = \
            (selection[0], selection[1], block_data)

        additions = []

    @property
    def json(self):
        return (self.main_block[0].__name__,
                list(self.main_block[1]),
                {name: [values[0], values[1]] for name, values in self.main_block[2].items()})

    @property
    def image(self) -> pygame.surface.Surface:
        return self.main_block[0].base_image


class TileMenu(Gui.Menu):
    def __init__(self, save_block):
        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect = pygame.Rect(top_left, (width, height))
        self.buttons = {}
        self.active = False
        self.current = None
        self.background = pygame.transform.scale(pygame.image.load("sprites/Gui/BlocksMenu.png"), self.rect.size)

        self.columns = 1
        # button areas
        self.button_margin = 5
        self.button_count = 1
        self.box_size = width / (self.columns + 1)
        self.save_block = save_block
        self.data = None

    def add_setting(self, obj: str, connection, func, params, kwargs):
        rect = pygame.rect.Rect(self.rect.left + self.box_size * (self.button_count % self.columns),
                                self.rect.top + self.box_size * ((self.button_count - 1) // self.columns),
                                self.box_size, self.box_size)

        if obj == "Button":
            button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin), (func, params, kwargs))
            self.buttons[button_1] = connection
        self.button_count += 1

    def save_current(self):
        data = {}
        for key, item in self.data[1].items():
            data[key] = item[0]

        self.save_block(self.data[0], data, self.data[0].base_image)

    def reset(self, tile: EditorTile):
        self.active = True
        self.current = tile
        self.buttons.clear()
        self.button_count = 1
        self.data = (tile.main_block[0], tile.main_block[2])

        data = {}
        for key, item in tile.main_block[2].items():
            data[key] = item[0]
        self.add_setting("Button", None, self.save_current, (), {})
        for name, (value, possible_values, swapper) in tile.main_block[2].items():
            func: callable = lambda: 0
            if isinstance(swapper, Iterable):
                def func():
                    a = next(swapper)
                    tile.main_block[2][name][:] = [a, possible_values, swapper]
            self.add_setting("Button", tile.main_block[2][name], func, (), {})

    def display(self, display_surface: pygame.surface.Surface):
        display_surface.blit(self.background, self.rect)
        for button, value in self.buttons.items():
            display_surface.blit(button.image, button.rect)
            if value is None:
                continue
            img = pygame.surface.Surface(button.rect.size)
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

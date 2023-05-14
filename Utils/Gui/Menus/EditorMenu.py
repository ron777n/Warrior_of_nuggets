"""
The menu for the editor
"""
import typing
from collections.abc import Iterable

import pygame.display
import pymunk

from physics.objects import BaseObject, DEFAULT_BLOCK_PATH, Solid
from settings import *
from Utils import Gui
from Utils.Gui import ImageSetting, NumberSetting, OptionSettings, Text

margin = 0
width = 192
width1 = 128
height = SCREEN_HEIGHT - margin
height1 = 128


class EditorMenu(Gui.Menu):
    """
    The menu class for the editor
    """

    def __init__(self, set_functions: tuple[callable, ...], *shapes: type[pymunk.Shape]):
        self.selected_block = None
        self.buttons: dict[Gui.BaseGui, tuple[type, dict]] = {}  # Button: data
        self.objects = []
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
        self.background1 = pygame.Surface(self.button_rect.size)
        self.background1.fill("#1C2833")

        self.create_block = set_functions[0]
        self.set_player = set_functions[1]
        self.delete_block = set_functions[2]
        self.start_button = set_functions[3]
        self.save_level = set_functions[4]

        self.create_buttons(shapes)

    def add_button(self, shape_constructor, values):
        rect = pygame.rect.Rect(
            self.scroll_rect.left + self.box_size * (self.buttons_i % self.columns),
            self.scroll_rect.top + self.box_size * (self.buttons_i // self.columns),
            self.box_size,
            self.box_size
        )
        annotations = shape_constructor.__annotations__
        for key, value in shape_constructor.__kwdefaults__.items():
            if key in annotations:
                annotation = annotations[key]
                annotation = annotation.__name__
                if key == "image":
                    value = (value, DEFAULT_BLOCK_PATH)
                if key in values:
                    value = values[key]

                values[key] = (value, annotation)

        img = values["image"][0][0]

        button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin),
                              lambda: self.create_block(shape_constructor, values), image=img)
        for button, (block_type, data) in self.buttons.items():
            if block_type == shape_constructor:
                for key in values:
                    if key == "image":
                        if data[key][0][1] != values[key][0][1]:
                            break
                        continue
                    if key not in data:
                        return
                    if data[key][0] != values[key][0]:
                        break
                else:
                    return
                continue
        self.buttons[button_1] = (shape_constructor, values)
        self.buttons_i += 1

    def add_object(self, func: (callable, Iterable, dict), image_path):
        rect = pygame.rect.Rect(
            self.button_rect.left + self.box_size * (self.object_i % self.columns1),
            self.button_rect.top + self.box_size * ((self.object_i - 1) // self.columns1),
            self.box_size,
            self.box_size)

        base_image = pygame.image.load(image_path)
        set_image = pygame.transform.scale(base_image, rect.size)
        button_1 = Gui.Button(rect.inflate(-self.button_margin, -self.button_margin),
                              lambda: func[0](*func[1], **func[2]), image=set_image)
        self.objects.append(button_1)
        self.object_i += 1

    def create_buttons(self, shapes):
        """
        just creates all the buttons
        """
        self.add_object((self.set_player, (), {}), "sprites/Gui/Buttons/ButtonPlayer.png")

        self.add_object((self.delete_block, (), {}), "sprites/Gui/Buttons/ButtonErase.png")

        self.add_object((self.start_button, (), {},),  "sprites/Gui/Buttons/ButtonStart.png")

        self.add_object((self.save_level, (), {},), "sprites/Gui/Buttons/ButtonSave.png")

        for i, shape_constructor in enumerate(shapes, start=1):
            self.add_button(shape_constructor, {})

    def display(self, display_surface):
        """
        puts everything on the screen
        """
        display_surface.blit(self.background, self.scroll_rect)
        display_surface.blit(self.background1, self.button_rect)

        for button in self.buttons:
            display_surface.blit(button.image, button.rect)
        for object_gui in self.objects:
            display_surface.blit(object_gui.image, object_gui.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        clicks all the inputs on the menu
        """
        r = self.collide_point(location)
        for button in self.buttons:
            r = button.click(location, button_type, down) or r
        for object_gui in self.objects:
            r = object_gui.click(location, button_type, down) or r
        return r

    def collide_point(self, point):
        return self.scroll_rect.collidepoint(point) or self.button_rect.collidepoint(point)

    def get_buttons(self) -> list:
        to_ret = []
        for block, data in self.buttons.values():
            to_ret.append((block.__name__, {key: (val if key != "image" else (val[0][1], *val[1:])) for key, val in data.items()}))
        return to_ret


class EditorTile:
    """
    The editor tile, handles what's in the specific tile
    """

    def __init__(self, selection: tuple[type(Solid), tuple, dict[any, tuple[any, tuple]]]):
        block_data = {}
        for key, (value, possible_values) in selection[2].items():
            data_swap = None
            if isinstance(possible_values, str):
                if possible_values == "int":
                    data_swap = NumberSetting
                elif possible_values == "Surface":
                    data_swap = ImageSetting
                # else:
                #     continue
            elif isinstance(possible_values, Iterable):
                data_swap = OptionSettings
            # if data_swap is not None:
            block_data[key] = [value, possible_values, data_swap]
        self.main_block: tuple[type(Solid), tuple, dict[any, list[any, any, any]]] = \
            (selection[0], selection[1], block_data)

        additions = []

    @property
    def json(self):
        return (self.main_block[0].__name__,
                list(self.main_block[1]),
                {name: [(values[0] if name != "image" else values[0][1]), values[1]] for name, values in
                 self.main_block[2].items() if not isinstance(values[0], pygame.Surface)})

    @property
    def image(self) -> pygame.surface.Surface:
        return self.main_block[2]["image"][0][0]


class TileMenu(Gui.Menu):
    def __init__(self, save_block):
        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect = pygame.Rect(top_left, (width, height))
        self.buttons = []
        self.active = False
        self.current = None
        self.background = pygame.transform.scale(pygame.image.load("sprites/Gui/BlocksMenu.png"), self.rect.size)

        self.columns = 1
        # button areas
        self.button_margin = 5
        self.add_location = 0
        self.row_count = 1
        self.box_size = width
        self.save_block = save_block
        self.data = None

    def add_setting(self, connection):
        scale = connection[2].scale
        rect = pygame.rect.Rect(self.rect.left + self.box_size * (self.row_count % self.columns),
                                self.rect.top + self.add_location,
                                self.box_size, self.box_size * scale)

        button = connection[2](rect, connection)
        self.buttons.append(button)
        self.add_location += rect.height
        # self.row_count = (self.row_count + 1) % self.columns

    def save_current(self):
        data = {}
        for key, item in self.data[1].items():
            data[key] = item[0]
        self.save_block(self.data[0], data)

    def reset(self, tile: EditorTile):
        self.active = True
        self.current = tile
        self.buttons.clear()
        self.add_location = 0
        self.row_count = 1
        self.data = (tile.main_block[0], tile.main_block[2])

        data = {}
        for key, item in tile.main_block[2].items():
            data[key] = item[0]
        save_btn = Gui.Button(pygame.Rect(self.rect.topleft, (self.rect.width, self.rect.width / 2)), self.save_current)
        add_text = Gui.Text("Save Block to collection")
        add_text.wrap(save_btn.rect.size).draw(save_btn.base_image)
        self.buttons.append(save_btn)
        self.add_location += self.rect.width / 2
        for name, connection in tile.main_block[2].items():
            if connection[2] is None:
                continue
            self.add_setting(connection)

    def display(self, display_surface: pygame.surface.Surface):
        display_surface.blit(self.background, self.rect)
        for button in self.buttons:
            display_surface.blit(button.image, button.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
        for button in self.buttons:
            r = button.click(location, button_type, down) or r
        return r

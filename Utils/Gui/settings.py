import itertools
from tkinter import filedialog

import pygame

from .basis import BaseGui, Button
from Utils.image_utils import Text

margin = 5


class NumberSetting(BaseGui):
    def __init__(self, rect: pygame.Rect, connection: list,
                 background_image: pygame.Surface = pygame.Surface((50, 50))):
        self.rect = rect.copy()
        self.background_image = pygame.transform.scale(background_image, self.rect.size)
        self.buttons_diff = self.rect.size[0] // 3
        button_rect = pygame.Rect(self.rect.topleft, (self.buttons_diff, self.rect.size[0]))
        button_rect = button_rect.inflate(-margin, -margin)
        self.reduce_button = Button(button_rect, lambda: self.add_to_val(-5))
        self.add_button = Button(button_rect.move((self.buttons_diff * 2, 0)), lambda: self.add_to_val(5))
        self.connection = connection

    def add_to_val(self, increment):
        self.connection[0] += increment

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        When user clicks the gui
        """
        collided = self.rect.collidepoint(location)
        self.add_button.click(location, button_type, down)
        self.reduce_button.click(location, button_type, down)
        return collided

    @property
    def image(self) -> pygame.Surface:
        img = self.background_image.copy()
        img.fill("red")
        img.blit(self.reduce_button.image, (0, 0))

        val_text = Text(str(self.connection[0]))
        img.blit(val_text, (self.buttons_diff * 1, 0))

        img.blit(self.add_button.image, (self.buttons_diff * 2, 0))
        return img


class OptionSettings(BaseGui):
    def __init__(self, rect: pygame.Rect, connection, background=pygame.Surface((50, 50))):
        self.background_image = pygame.transform.scale(background, rect.size)
        self.current_value = connection[0]
        self._swapper = itertools.cycle(connection[1])
        self.rect = rect.copy()
        rect = pygame.Rect(rect.topleft, (rect.size[0] // 2, rect.size[1]))
        rect = rect.inflate(-margin, -margin)
        self.button = Button(rect, self.next, pygame.image.load("sprites/Gui/Button.png"))
        self.connection = connection

    def next(self):
        a = next(self._swapper)
        self.current_value = a
        self.connection[0] = a
        return a

    @property
    def image(self):
        img = self.background_image.copy()
        img.fill("red")
        img.blit(self.button.image, (0, 0))
        text = Text(self.current_value)
        img.blit(text, (self.rect.size[0] / 2, 0))
        return img

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        collided = self.rect.collidepoint(location)
        self.button.click(location, button_type, down)

        return collided


class FileSetting(BaseGui):
    def __init__(self, rect: pygame.Rect, connection, background=pygame.Surface((50, 50))):
        self.background_image = pygame.transform.scale(background, rect.size)
        self.rect = rect.copy()
        self.connection = connection
        self.base_button_image = pygame.transform.scale(pygame.image.load("sprites/Gui/Button.png"), self.rect.size)
        self.button = Button(rect, self.set_file, self.base_button_image)
        self.update_button_image(self.connection[0])

    def update_button_image(self, path: str):
        img = self.base_button_image.copy()
        text = Text(path[path.rfind("/") + 1:])
        img.blit(text, (0, 0))
        self.button.base_image = img

    def set_file(self):
        path = filedialog.askopenfilename()
        self.update_button_image(path)
        self.connection[0] = path

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        collided = self.rect.collidepoint(location)
        self.button.click(location, button_type, down)

        return collided

    @property
    def image(self) -> pygame.Surface:
        img = self.background_image.copy()
        img.blit(self.button.image, (0, 0))
        return img

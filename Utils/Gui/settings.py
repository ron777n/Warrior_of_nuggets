import itertools
from tkinter import filedialog

import pygame

from .basis import BaseGui, Button
from .image_utils import Text

margin = 5


class BaseSetting(BaseGui):
    scale: float

    def __init__(self, rect: pygame.Rect, connection: list):
        self.rect = rect.copy()
        self.connection = connection

    @property
    def image(self):
        return pygame.Surface(self.rect.size, pygame.SRCALPHA)


class NumberSetting(BaseSetting):
    scale = 0.2

    def __init__(self, rect: pygame.Rect, connection: list):
        super().__init__(rect, connection)
        self.buttons_diff = self.rect.size[0] // 3
        button_rect = pygame.Rect(self.rect.topleft, (self.buttons_diff, self.rect.size[1]))
        button_rect = button_rect.inflate(-margin, -margin)
        self.reduce_button = Button(button_rect, lambda: self.add_to_val(-5))
        self.add_button = Button(button_rect.move((self.buttons_diff * 2, 0)), lambda: self.add_to_val(5))

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
        img = super().image
        img.blit(self.reduce_button.image, (0, 0))

        val_text = Text(str(self.connection[0]))
        val_text.draw(img)

        img.blit(self.add_button.image, (self.buttons_diff * 2, 0))
        return img


class OptionSettings(BaseSetting):
    scale = 0.2

    def __init__(self, rect: pygame.Rect, connection):
        super().__init__(rect, connection)
        self._swapper = itertools.cycle(connection[1])
        for i in self._swapper:
            if i == self.connection[0]:
                break
        self.button = Button(rect, self.next, pygame.image.load("sprites/Gui/Button.png"))
        self.base_button_image = self.button.base_image
        self.connection = connection
        self.update_image(self.connection[0])

    def update_image(self, val):
        img = self.base_button_image.copy()
        text = Text(val)
        text.draw(img)
        self.button.base_image = img

    def next(self):
        a = next(self._swapper)
        self.update_image(a)
        self.connection[0] = a
        return a

    @property
    def image(self):
        img = super().image
        img.blit(self.button.image, (0, 0))
        return img

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        collided = self.rect.collidepoint(location)
        self.button.click(location, button_type, down)

        return collided


class FileSetting(BaseSetting):
    scale = 0.3

    def __init__(self, rect: pygame.Rect, connection, background=pygame.Surface((50, 50))):
        super().__init__(rect, connection)
        self.background_image = pygame.transform.scale(background, rect.size)
        self.connection = connection
        self.base_button_image = pygame.transform.scale(pygame.image.load("sprites/Gui/Button.png"), self.rect.size)
        self.button = Button(rect, self.set_file, self.base_button_image)
        self.update_button_image(self.connection[0])

    def update_button_image(self, path: str):
        img = self.base_button_image.copy()
        text = Text(path[path.rfind("/") + 1:])
        text.draw(img)
        self.button.base_image = img

    def set_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        self.update_button_image(path)
        self.connection[0] = path

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        collided = self.rect.collidepoint(location)
        self.button.click(location, button_type, down)

        return collided

    @property
    def image(self) -> pygame.Surface:
        img = super().image
        img.blit(self.button.image, (0, 0))
        return img


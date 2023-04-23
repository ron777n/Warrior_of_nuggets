"""
Handler for the basic classes for the gui
"""
import abc
from typing import Callable

import pygame


class BaseGui(pygame.sprite.Sprite, abc.ABC):
    """
    The base gui class
    """
    _rect: pygame.Rect

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        When user clicks the gui
        """
        pass

    def scroll(self, location, amount):
        """
        If user scrolls on the screen
        """
        pass

    @property
    def image(self) -> pygame.surface.Surface:
        """
        returns the image to display of the object
        """
        return pygame.surface.Surface((50, 50))

    @property
    def rect(self) -> pygame.rect.Rect:
        """
        the rect of the object
        """
        return self._rect

    @rect.setter
    def rect(self, rect: pygame.rect.Rect):
        self._rect = rect


class Button(BaseGui):
    """
    simple object that is clickable
    """
    def __init__(self, rect: pygame.Rect, on_click, *groups, image: pygame.Surface = pygame.Surface((50, 50))):
        super().__init__(*groups)
        self.on_click: callable
        if callable(on_click):
            self.on_click = on_click
        else:
            self.on_click = lambda: on_click[0](*on_click[1:])
        self.rect = rect.copy()
        self.clicked = False
        self._image = pygame.transform.scale(image, self.rect.size)

    def click(self, location: tuple[int, int], button_type: int, down: bool):
        """
        pass
        """
        collided = self.rect.collidepoint(location)
        if down:
            if collided:
                self.clicked = True
                self.on_click()
        else:
            self.clicked = False
        return collided

    @property
    def image(self):
        """
        little opacity while button held
        """
        alpha = 127 if self.clicked else 255
        img = self._image.copy()
        img.set_alpha(alpha)
        return img

"""
Handler for the basic classes for the gui
"""
import abc

import pygame


class BaseGui(pygame.sprite.Sprite, abc.ABC):
    """
    The base gui class
    """

    def click(self, mouse_data: tuple[tuple[int, int], tuple[int, int]]):
        """
        When user clicks the gui
        """
        pass

    def scroll(self, amount):
        """
        If user scrolls on the screen
        """
        pass

    @property
    def image(self) -> pygame.surface.Surface:
        return pygame.surface.Surface((50, 50))

    @property
    def rect(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(0, 0, 50, 50)

    @rect.setter
    def rect(self, other: pygame.rect.Rect):
        pass

"""
Handler for the basic classes for the gui
"""
import abc

import pygame


class BaseGui(pygame.sprite, abc.ABC):
    """
    The base gui class
    """

    def click(self, mouse_data: tuple[int, int, int]):
        """
        When user clicks the gui
        """
        pass

    def scroll(self, amount):
        """
        If user scrolls on the screen
        """
        pass

    def change_rect(self, new_rect):
        pass

    @property
    def image(self) -> pygame.surface.Surface:
        return pygame.surface.Surface((50, 50))

    @property
    def rect(self):
        return

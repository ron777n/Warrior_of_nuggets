"""
The menu for the editor
"""
import pygame.display

import physics.objects
from settings import *
from Utils import Gui
import itertools


class Menu:
    """
    The menu class for the editor
    """
    def __init__(self, *classes: list[type[physics.objects.BaseObject]]):
        self.display_surface = pygame.display.get_surface()
        self.rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.buttons: list[Gui.BaseGui] = []
        self.create_buttons(*classes)

    def create_buttons(self, *classes):
        """
        just creates all the buttons
        """
        # menu area
        size = 180
        margin = 6
        top_left = (SCREEN_WIDTH - size - margin, SCREEN_HEIGHT - size - margin)
        self.rect.update(top_left, (size, size))

        # button areas
        generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
        button_margin = 5

        buttons_data = []

        for i, class_type in enumerate(classes):
            (
                generic_button_rect.copy(),
                lambda: print(i, class_type),
                (255, 0, 0)
            )

        # buttons_data = (
        #     (
        #         generic_button_rect.copy(),
        #         lambda: print("clicked 1"),
        #         (255, 0, 0)
        #     ),
        #     (
        #         generic_button_rect.move(self.rect.width / 2, 0),
        #         lambda: print("clicked 2"),
        #         (0, 255, 0)
        #     ),
        #     (
        #         generic_button_rect.move(0, self.rect.height / 2),
        #         lambda: print("clicked 3"),
        #         (0, 0, 255)
        #     ),
        #     (
        #         generic_button_rect.move(self.rect.width / 2, self.rect.height / 2),
        #         lambda: print("clicked 4"),
        #         (255, 255, 0)
        #     ),
        # )
        for rect, function, color in buttons_data:
            image = pygame.surface.Surface((50, 50))
            image.fill(color)
            button_1 = Gui.Button(rect.inflate(-button_margin, -button_margin),
                                  function, image=image)
            self.buttons.append(button_1)

    def display(self):
        """
        puts everything on the screen
        """
        for button in self.buttons:
            self.display_surface.blit(button.image, button.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        clicks all the inputs on the menu
        """
        r = False
        for button in self.buttons:
            if button.click(location, button_type, down):
                r = True
        return r


"""
The menu for the editor
"""
import pygame.display

import physics.objects
from settings import *
from Utils import Gui


class Menu:
    """
    The menu class for the editor
    """

    def __init__(self, set_function: callable, *classes: type[physics.objects.BaseObject]):
        self.selected_block = None
        self.display_surface = pygame.display.get_surface()
        self.rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.buttons: list[Gui.BaseGui] = []
        self.create_buttons(set_function, *classes)

    def create_buttons(self, set_class, *classes):
        """
        just creates all the buttons
        """
        # menu area
        width = 180
        height = 180
        margin = 6
        columns = 2
        top_left = (SCREEN_WIDTH - width - margin, SCREEN_HEIGHT - height - margin)
        self.rect.update(top_left, (width, height))

        # button areas
        generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
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

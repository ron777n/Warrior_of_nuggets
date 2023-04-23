"""
The menu for the editor
"""
import pygame.display
from settings import *
from Utils import Gui


class Menu:
    """
    The menu class for the editor
    """
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)
        self.buttons: list[Gui.BaseGui] = []
        self.create_buttons()

    def create_buttons(self):
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

        button_1 = Gui.Button(generic_button_rect.copy().inflate(-button_margin, -button_margin),
                              lambda: print("clicked"))
        self.buttons.append(button_1)

        # self.buttons.append(generic_button_rect.copy().inflate(-button_margin, -button_margin))
        # self.buttons.append(generic_button_rect.move(self.rect.width / 2, 0).inflate(-button_margin, -button_margin))
        # self.buttons.append(generic_button_rect.move(0, self.rect.height / 2).inflate(-button_margin, -button_margin))
        # self.buttons.append(generic_button_rect.move(self.rect.width / 2, self.rect.height / 2).inflate(-button_margin, -button_margin))

    def display(self):
        """
        puts everything on the screen
        """
        # pygame.draw.rect(self.display_surface, "red", self.rect)
        for button in self.buttons:
            self.display_surface.blit(button.image, button.rect)

    def click(self, location: tuple[int, int], button_type: int, down: bool):
        """
        clicks all the inputs on the menu
        """
        for button in self.buttons:
            button.click(location, button_type, down)


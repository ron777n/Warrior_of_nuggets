"""
Handler for the basic classes for the gui
"""
import abc

import pygame


class BaseGui(abc.ABC):
    """
    The base gui class
    """
    rect: pygame.Rect
    image: pygame.Surface

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        When user clicks the gui
        """
        pass

    def scroll(self, location, amount) -> bool:
        """
        If user scrolls on the screen
        """
        pass

    def collide_point(self, point) -> bool:
        """
        checks if the point hits the gui
        """
        return self.rect.collidepoint(point)


class Button(BaseGui):
    """
    simple object that is clickable
    """

    def __init__(self, rect: pygame.Rect, on_click,
                 image: pygame.Surface = pygame.image.load("sprites/Gui/Button.png")):
        # super().__init__()
        self.on_click: callable
        if callable(on_click):
            self.on_click = on_click
        else:
            self.on_click = lambda: on_click[0](*on_click[1], **on_click[2])
        self.rect = rect.copy()
        self.clicked = False
        self.base_image = pygame.transform.scale(image, self.rect.size)

    def click(self, location: tuple[int, int], button_type: int, down: bool):
        """
        pass
        """
        collided = self.rect.collidepoint(location)
        if down:
            if collided and button_type == pygame.BUTTON_LEFT:
                self.clicked = True
        elif button_type == pygame.BUTTON_LEFT:
            self.clicked = False
            if collided:
                self.on_click()
        return collided

    @property
    def image(self):
        """
        little opacity while button held
        """
        alpha = 127 if self.clicked else 255
        img = self.base_image.copy()
        img.set_alpha(alpha)
        return img


class Menu(abc.ABC):
    def display(self, display_surface: pygame.surface.Surface):
        """
        displays the menu on the screen
        """
        ...

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        """
        clicks the menu
        """
        ...

    def collide_point(self, point):
        """
        if it hit the menu
        """
        ...

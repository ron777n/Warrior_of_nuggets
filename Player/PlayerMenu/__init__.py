import pygame

# from Player import Player
from Player.Inventory import Inventory
from Utils.Gui import Menu, Text


class InGameMenu(Menu):
    def __init__(self, player, inventory: Inventory):
        self.player = player
        self.inventory = inventory

    def display(self, display_surface):
        hand_left = self.inventory.hot_bar.items[0]
        hand_right = self.inventory.hot_bar.items[1]
        for i, item in enumerate(hand_left):
            if item is not None:
                display_surface.blit(pygame.transform.scale(item.image, (50, 50)), (i * 50, 0))
        for i, item in enumerate(hand_right):
            if item is not None:
                display_surface.blit(pygame.transform.scale(item.image, (50, 50)), (i * 50 + 25 + 50 * 3, 0))
        hp = self.player.health
        health_text = Text(str(hp), color=(0, 0, 0))
        health_text.draw(display_surface, ('center',))


class PlayerMenu(Menu):
    # active_menu: Menu = False

    def __init__(self, player):
        self.inventory = Inventory(player)
        self.game_menu = InGameMenu(player, self.inventory)
        self._active_menu = self.game_menu

    @property
    def active_menu(self) -> str:
        if self._active_menu is self.inventory:
            return "Inventory"
        elif self._active_menu is self.game_menu:
            return "Game"
        return "NONE"

    @active_menu.setter
    def active_menu(self, value: str):
        if value == "Inventory":
            value = self.inventory
        elif value == "Game":
            value = self.game_menu
        else:
            raise ValueError("Menu Type is not defined")
        self._active_menu = value

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        return self._active_menu.click(location, button_type, down)

    def display(self, surface):
        return self._active_menu.display(surface)

    def collide_point(self, point):
        return self._active_menu.collide_point(point)

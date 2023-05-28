from Player.Inventory import Inventory
from Utils.Gui import Menu


class InGameMenu(Menu):
    pass


class PlayerMenu(Menu):
    # active_menu: Menu = False

    def __init__(self, ):
        self.inventory = Inventory()
        self.game_menu = InGameMenu()
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

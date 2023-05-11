import pygame

from .basis import Item


class ShotGun(Item):
    image = pygame.image.load("sprites/objects/tools/guns/shotgun.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            print("SHOOT", start_pos, end_pos)
        return False

    def add_to_item(self, item) -> bool:
        return False


class Nugget(Item):
    image = pygame.image.load("sprites/objects/tools/food/Nugget.png")

    def __init__(self):
        self.count = 1

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            print("EAT NUGGET")
            self.count -= 1
            if not self.count:
                return True
        return False

    def add_to_item(self, item) -> bool:
        self.count += 1
        return True


__all__ = ["ShotGun", "Nugget"]

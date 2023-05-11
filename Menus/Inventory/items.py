import pygame

from .basis import Item


class ShotGun(Item):
    image = pygame.image.load("sprites/objects/tools/guns/shotgun.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool):
        if button == pygame.BUTTON_LEFT and down:
            print("SHOOT", start_pos, end_pos)


class Nugget(Item):
    image = pygame.image.load("sprites/objects/tools/food/Nugget.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool):
        if button == pygame.BUTTON_LEFT and down:
            print("EAT NUGGET")


__all__ = ["ShotGun", "Nugget"]

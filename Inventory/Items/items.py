import pygame
import pymunk

from physics.objects import Bullet
from ..basis import Item


class ShotGun(Item):
    image = pygame.image.load("sprites/objects/tools/guns/shotgun.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            vector = pymunk.Vec2d(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
            Bullet(self.space, self.camera, start_pos, vector.angle_degrees)
        return False

    def add_to_item(self, item) -> bool:
        return False


class Nugget(Item):
    image = pygame.image.load("sprites/objects/tools/food/Nugget.png")

    def __init__(self, space, camera, owner, count=1):
        super().__init__(space, camera, owner)
        self.count = count

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            print("EAT NUGGET")
            self.owner.heal(30)
            self.count -= 1
            if not self.count:
                return True
        return False

    def add_to_item(self, item) -> bool:
        self.count += 1
        return True


class Knife(Item):
    image = pygame.image.load("sprites/objects/tools/Weapons/Knife.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT:
            pass
        elif button == pygame.BUTTON_RIGHT:
            self.owner.damage(20)
        return False


__all__ = ["ShotGun", "Nugget", "Knife"]

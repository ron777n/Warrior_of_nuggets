import pygame
import pymunk

from physics.objects import NoGravity
from .Logic import Bullet
from ...basis import Item


class ShotGun(Item):
    image = pygame.image.load("sprites/objects/tools/guns/shotgun.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            vector = pymunk.Vec2d(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
            Bullet(self.owner, self.camera, self.space, start_pos, vector.angle_degrees, NoGravity())
        return False

    def add_to_item(self, item) -> bool:
        return False

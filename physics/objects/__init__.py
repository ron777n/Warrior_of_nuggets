"""
pass
"""

import pygame
import pymunk

from Utils import image_utils


class BaseObject(pymunk.Body):
    @property
    def image(self) -> pygame.surface.Surface:
        return pygame.surface.Surface((50, 50))


class Solid(BaseObject):
    base_image: pygame.surface.Surface

    def __init__(self, space, rect: pygame.rect.Rect, *, mass=0.1, moment=0, body_type=pymunk.Body.DYNAMIC):
        super().__init__(mass=mass, moment=moment, body_type=body_type)
        self.shape = pymunk.Poly.create_box(self, size=rect.size)
        self.shape.mass = 1
        self.position = rect.center
        self._rect = rect
        self.original_size = rect.size
        space.add(self, self.shape)

    @property
    def rect(self) -> pygame.rect.Rect:
        return self._rect.copy()

    @property
    def image(self):
        img = pygame.transform.scale(self.base_image.copy(), (self.original_size[0], self.original_size[1]))
        img = pygame.transform.rotate(img, int(-self.rotation_vector.angle_degrees))
        self._rect.size = img.get_size()
        self._rect.center = self.position[0], self.position[1]
        return img


class Block(Solid):
    base_image = pygame.image.load("sprites/objects/block.png")


class SlipperyBlock(Block):
    base_image = image_utils.tint_image(Block.base_image, (0, 0, 255), 200)

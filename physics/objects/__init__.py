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

    def __init__(self, space, rect: pygame.rect.Rect, *, mass=1, moment=0, body_type=pymunk.Body.DYNAMIC):
        super().__init__(mass=mass, moment=moment, body_type=body_type)
        self.shape = pymunk.Poly.create_box(self, size=rect.size)
        self.shape.mass = 1
        self.position = rect.center
        self._rect = rect
        space.add(self, self.shape)

    @property
    def rect(self) -> pygame.rect.Rect:
        return self._rect

    @property
    def image(self):
        img = self.base_image
        if self._rect.size != (0, 0):
            img = pygame.transform.scale(img, self._rect.size)
        # img = pygame.transform.rotate(img, -self.rotation_vector.angle_degrees)
        if self._rect.size != (img_rect_size := img.get_rect().size):
            self._rect.size = img_rect_size[0] + self._rect.size[0] // 2, img_rect_size[1] + self._rect.size[1] // 2
        self._rect.center = self.position
        return img


class Block(Solid):
    base_image = pygame.image.load("sprites/objects/block.png")


class SlipperyBlock(Block):
    base_image = image_utils.tint_image(Block.base_image, (0, 0, 255), 200)

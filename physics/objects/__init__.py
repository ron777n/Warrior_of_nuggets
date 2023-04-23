"""
pass
"""

import pygame
import pymunk


class BaseObject(pymunk.Body):

    @property
    def image(self) -> pygame.surface.Surface:
        return pygame.surface.Surface((50, 50))


class Solid(BaseObject):
    _image: pygame.surface.Surface

    @property
    def rect(self) -> pygame.rect.Rect:
        return pygame.rect.Rect(0, 0, 50, 50)

    @property
    def image(self):
        img = self._image
        if self.size != (0, 0):
            img = pygame.transform.scale(img, self.size)
        img = pygame.transform.rotate(img, self.image_angle)
        if self.rect.size != (img_rect_size := img.get_rect().size):
            self.rect.size = Vector2(Vector2(img_rect_size) + Vector2(self.rect.size)) // 2
        self.rect.center = self.position
        return img


class Block(Solid):
    pass

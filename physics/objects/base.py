import abc

import pygame
import pymunk


class BaseObject(abc.ABC):
    rect: pygame.Rect
    image: pygame.Surface

    def update(self):
        pass


def shape_rect(self: pymunk.Shape) -> pygame.rect.Rect:
    left, bottom, right, top = self.cache_bb()
    size = right - left, top - bottom
    rect = pygame.rect.Rect((left, top - size[1]), size)
    return rect


def shape_image(self: pymunk.Shape) -> pygame.Surface:
    img = self.base_image.copy()
    img = pygame.transform.rotate(img, -self.body.rotation_vector.angle_degrees)
    return img


pymunk.Shape.rect = property(shape_rect)
pymunk.Shape.image = property(shape_image)


def block_shape(body, size, *, mass: int = 100, friction: float = 0.95,
                elasticity: float = 0.0) -> any:
    shape: pygame.Poly = pymunk.Poly.create_box(body, size)
    shape.mass = mass
    shape.friction = friction
    shape.elasticity = elasticity
    return shape

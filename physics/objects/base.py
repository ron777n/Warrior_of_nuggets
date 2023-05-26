import abc

import pygame
import pymunk

from Utils.Timers import Timer


class BaseObject(abc.ABC):
    rect: pygame.Rect
    image: pygame.Surface

    def update(self, dt):
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


class Effect:
    timeout: 1000

    def __init__(self, *effects: 'Effect', timeout=None):
        self.effects = effects
        if timeout is None:
            self.timer = Timer(self.timeout)
        else:
            self.timer = Timer(timeout)

    def effect(self, body, dt):
        if self.timer.has_expired():
            return False
        for effect in self.effects:
            effect.effect(body, dt)
        return True

    def __add__(self, other: 'Effect') -> 'Effect':
        timeout = min(self.timeout, other.timeout)
        return Effect(*self.effects + (other,), timeout=timeout)

    def __hash__(self):
        return hash(self.effects)

    def __eq__(self, other: 'Effect'):
        return self.effects == other.effects

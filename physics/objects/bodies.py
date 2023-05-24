import math

import pygame
import pymunk

from .base import BaseObject
from .effects import Effect

DEFAULT_BLOCK_PATH = "sprites/objects/block.png"


class Solid(BaseObject, pymunk.Body):
    base_image: pygame.surface.Surface

    def __init__(self, space: pymunk.Space, position,
                 *shapes, body_type_name: str = "STATIC", mass=0, moment=0, image_path=DEFAULT_BLOCK_PATH):
        body_type: int = getattr(pymunk.Body, body_type_name)
        super().__init__(body_type=body_type, mass=mass, moment=moment)

        for shape in shapes:
            shape.body = self

        self.effects: set['Effect'] = set()

        self.base_image: pygame.Surface = pygame.transform.scale(pygame.image.load(image_path), self.rect.size)
        self.position = pymunk.vec2d.Vec2d(*position)
        space.add(self, *self.shapes)

    def update(self, dt):
        for effect in self.effects.copy():
            if not effect.effect(self, dt):
                self.effects.remove(effect)

    def add_effect(self, effect):
        for effect_ in self.effects:
            if effect == effect_:
                effect_.timer.reset()
                break
        else:
            self.effects.add(effect)

    def remove_effect(self, effect):
        self.effects.remove(effect)

    @property
    def rect(self) -> pygame.rect.Rect:
        inf = float("inf")
        top, left, bottom, right = inf, inf, -inf, -inf
        for shape in self.shapes:
            current_shape_rect = shape.rect
            top = min(top, current_shape_rect.top)
            left = min(left, current_shape_rect.left)
            bottom = max(bottom, current_shape_rect.bottom)
            right = max(right, current_shape_rect.right)
        rect = pygame.rect.Rect(left, top, right - left, bottom - top)
        return rect

    @property
    def image(self):
        img = pygame.transform.rotate(self.base_image.copy(), -self.rotation_vector.angle_degrees)
        return img

    def hit_global(self, impulse_vector, global_position, can_damage=False):
        if self.body_type == pymunk.Body.STATIC:
            return
        self.apply_impulse_at_world_point(impulse_vector, global_position)
        if can_damage:
            self.damage_local(abs(impulse_vector), self.world_to_local(global_position))

    def damage_local(self, power, position=(0, 0)):
        pass

    def hit_local(self, impulse_vector, local_position, can_damage=False):
        if self.body_type == pymunk.Body.STATIC:
            return
        self.apply_impulse_at_local_point(impulse_vector, local_position)
        if can_damage:
            if isinstance(impulse_vector, tuple):
                force = math.sqrt(impulse_vector[0] ** 2 + impulse_vector[1] ** 2)
            else:
                force = abs(impulse_vector)
            self.damage_local(force, self.world_to_local(local_position))

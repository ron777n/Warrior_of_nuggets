"""
pass
"""
import abc
import os
from typing import Literal

import pygame
import pymunk

from Utils.Timers import Timer


class BaseObject(abc.ABC):
    rect: pygame.Rect
    image: pygame.Surface


class Solid(BaseObject, pymunk.Body):
    base_image: pygame.surface.Surface = pygame.image.load("sprites/objects/block.png")

    def __init__(self, space, rect: pygame.rect.Rect, *, mass: int = 100,
                 body_type: Literal["DYNAMIC", "STATIC"] = "STATIC", friction: float = 0.95,
                 image_path: os.PathLike = "sprites/objects/block.png"):
        body_type = getattr(pymunk.Body, body_type)
        super().__init__(mass=mass, body_type=body_type)
        self.shape = pymunk.Poly.create_box(self, size=rect.size)
        self.shape.mass = mass
        self.shape.friction = friction
        self.position = pymunk.vec2d.Vec2d(*rect.center)
        self._rect = rect
        self.original_size = rect.size
        space.add(self, self.shape)
        self.base_image = pygame.image.load(image_path)

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


class Bullet(BaseObject):
    DE_SPAWN_TIMER = 10

    def __init__(self, space, camera, spawn, angle):
        vector = pymunk.Vec2d(1, 0).rotated_degrees(angle)
        got = sorted(space.segment_query(spawn, tuple(spawn + vector.scale_to_length(1000)), 3,
                                         pymunk.ShapeFilter()), key=lambda x: abs(x.point - spawn))
        hit: pymunk.SegmentQueryInfo
        self.start_pos = spawn

        if len(got) < 2:
            size = vector.int_tuple
            self.end_pos = (abs(size[0]), abs(size[1]))
            self.rect = pygame.Rect(spawn, self.end_pos)
            self.camera = camera
            self.camera.append(self)
            self.death_timer = Timer(self.DE_SPAWN_TIMER)
            return
        hit = got[0]
        self.end_pos = hit.point
        hit_body = hit.shape.body
        hit_body.apply_impulse_at_world_point(vector.scale_to_length(1000), self.end_pos)
        rect_location = min(self.end_pos[0], spawn[0]), min(self.end_pos[1], spawn[1])
        rect_size = (self.end_pos - spawn).int_tuple
        rect_size = abs(rect_size[0]), abs(rect_size[1])
        self.rect = pygame.Rect(rect_location, rect_size)
        self.camera = camera
        self.camera.append(self)
        self.death_timer = Timer(self.DE_SPAWN_TIMER)

    @property
    def image(self) -> pygame.Surface:
        img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.line(img, (255, 0, 0), pymunk.Vec2d(*self.start_pos) - self.rect.topleft,
                         pymunk.Vec2d(*self.end_pos) - self.rect.topleft)
        if self.death_timer.has_expired():
            self.camera.remove(self)
            return img
        return img

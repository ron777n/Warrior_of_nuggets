from typing import Optional

import pygame
import pymunk

from Utils.Timers import Timer
from .base import BaseObject
from .bodies import Solid
from .effects import NoGravity


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
        hit_body: Optional[Solid] = hit.shape.body
        if hit_body is None:
            return
        hit_body.hit_global(vector.scale_to_length(1000), self.end_pos)
        hit_body.add_effect(NoGravity())
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

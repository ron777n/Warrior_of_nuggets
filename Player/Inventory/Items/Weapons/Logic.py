from typing import Optional

import pygame
import pymunk

from physics.objects import BaseObject, ray_trace, ray_trace_first, Solid
from Utils.Timers import Timer


class Bullet(BaseObject):
    DE_SPAWN_TIMER = 10

    def __init__(self, source, camera, space, spawn, angle, effect=None):
        vector = pymunk.Vec2d(1000, 0).rotated_degrees(angle)
        self.start_pos = spawn

        hit: pymunk.SegmentQueryInfo
        hit = ray_trace_first(space, spawn, vector, source)
        if hit is None:
            self.end_pos = spawn + vector
            self.rect = self.create_camera_rect(spawn, self.end_pos)

            self.camera = camera
            self.camera.append(self)
            self.death_timer = Timer(self.DE_SPAWN_TIMER)
            return
        hit_body = hit.shape.body
        self.end_pos = hit.point
        if hit_body is None:
            return
        hit_body.hit_global(vector, self.end_pos)
        if effect is not None:
            hit_body.add_effect(effect)
        self.rect = self.create_camera_rect(spawn, self.end_pos)
        self.camera = camera
        self.camera.append(self)
        self.death_timer = Timer(self.DE_SPAWN_TIMER)

    @staticmethod
    def create_camera_rect(start_pos, end_pos):
        rect_location = min(end_pos[0], start_pos[0]), min(end_pos[1], start_pos[1])
        rect_size = (end_pos - start_pos).int_tuple
        rect_size = abs(rect_size[0]), abs(rect_size[1])
        return pygame.Rect(rect_location, rect_size)

    @property
    def image(self) -> pygame.Surface:
        img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.line(img, (255, 0, 0), pymunk.Vec2d(*self.start_pos) - self.rect.topleft,
                         pymunk.Vec2d(*self.end_pos) - self.rect.topleft)
        if self.death_timer.has_expired():
            self.camera.remove(self)
            return img
        return img

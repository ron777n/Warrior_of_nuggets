"""
pass
"""
import abc
from typing import Optional

import pygame
import pymunk

from Utils.Timers import Timer


class BaseObject(abc.ABC):
    rect: pygame.Rect
    image: pygame.Surface


def shape_rect(self: pymunk.Shape) -> pygame.rect.Rect:
    left, bottom, right, top = self.cache_bb()
    size = right - left, top - bottom
    rect = pygame.rect.Rect((left, top - size[1]), size)
    return rect


def shape_image(self: pymunk.Shape) -> pygame.Surface:
    img = self.base_image.copy()
    return img


pymunk.Shape.rect = property(shape_rect)
pymunk.Shape.image = property(shape_image)

DEFAULT_BLOCK_PATH = "sprites/objects/block.png"


def block(body, size, *, mass: int = 100, friction: float = 0.95,
          elasticity: float = 0.0, image: pygame.Surface = pygame.image.load(DEFAULT_BLOCK_PATH)) -> any:
    shape: pygame.Poly = pymunk.Poly.create_box(body, size)
    setattr(shape, "base_image", pygame.transform.scale(image, size))
    shape.mass = mass
    shape.friction = friction
    shape.elasticity = elasticity

    return shape


class Solid(BaseObject, pymunk.Body):
    base_image: pygame.surface.Surface = pygame.image.load("sprites/objects/block.png")

    def __init__(self, space: pymunk.Space, position,
                 *shapes, body_type_name: str = "STATIC", mass=0, moment=0):
        body_type: int = getattr(pymunk.Body, body_type_name)
        super().__init__(body_type=body_type, mass=mass, moment=moment)

        for shape in shapes:
            shape.body = self

        self.position = pymunk.vec2d.Vec2d(*position)
        space.add(self, *self.shapes)

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
        # print(self.shapes, current_shape_rect, rect)
        return rect

    @property
    def image(self):
        rect = self.rect
        img = pygame.Surface(rect.size, pygame.SRCALPHA)
        for shape in self.shapes:
            img.blit(shape.image, shape.rect.topleft - pymunk.Vec2d(*rect.topleft))
        return img

    def hit_global(self, impulse_vector, global_position):
        local_position = self.world_to_local(global_position)
        self.hit_local(impulse_vector, local_position)

    def hit_local(self, impulse_vector, local_position):
        self.apply_impulse_at_local_point(impulse_vector, local_position)


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

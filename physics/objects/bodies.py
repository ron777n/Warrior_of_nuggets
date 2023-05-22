import pygame
import pymunk

from physics.objects import BaseObject

DEFAULT_BLOCK_PATH = "sprites/objects/block.png"


class Solid(BaseObject, pymunk.Body):
    base_image: pygame.surface.Surface

    def __init__(self, space: pymunk.Space, position,
                 *shapes, body_type_name: str = "STATIC", mass=0, moment=0, image_path=DEFAULT_BLOCK_PATH):
        body_type: int = getattr(pymunk.Body, body_type_name)
        super().__init__(body_type=body_type, mass=mass, moment=moment)

        for shape in shapes:
            shape.body = self

        self.base_image: pygame.Surface = pygame.transform.scale(pygame.image.load(image_path), self.rect.size)
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
        return rect

    @property
    def image(self):
        img = pygame.transform.rotate(self.base_image.copy(), -self.rotation_vector.angle_degrees)
        return img

    def hit_global(self, impulse_vector, global_position):
        local_position = self.world_to_local(global_position)
        self.hit_local(impulse_vector, local_position)

    def hit_local(self, impulse_vector, local_position):
        self.apply_impulse_at_local_point(impulse_vector, local_position)

import pymunk

from .basis import Magic
from ..objects import exclusion_filter, ray_trace_first, Solid


class PushMagic(Magic):
    mana_usage = 30

    def cast(self):
        if not super().cast():
            return False
        direction: pymunk.Vec2d = self.source.camera.get_mouse_pos(mid=True)
        hit = ray_trace_first(self.source.space, self.source.position, direction, self.source)
        if hit is None or hit.shape.body.body_type == pymunk.Body.STATIC:
            return False
        hit_body: Solid | None = hit.shape.body
        hit_body.hit_global(direction.scale_to_length(1000), hit.point)
        self.source.mana -= self.mana_usage
        return False


class HoldMagic(Magic):
    mana_usage = 3

    def __init__(self, source: Solid, target_rect):
        super().__init__(source)
        self.target_rect = target_rect
        self.target_body = None

    def cast(self):
        if not super().cast():
            return False
        position = self.source.camera.get_mouse_pos(global_pos=True)
        hit = self.source.space.point_query_nearest(position, 20, pymunk.ShapeFilter())
        if hit is None or hit.shape.body.body_type == pymunk.Body.STATIC:
            return False
        hit_body: Solid | None = hit.shape.body
        self.target_body = hit_body
        return True

    def update(self, dt):
        print(self.source.mana)
        if self.source.mana < self.mana_usage:
            self.target_body = None
            return False
        self.target_body.hit_global((self.target_rect.center - self.target_body.position).scale_to_length(100) * dt - self.target_body.space.gravity * self.target_body.mass * dt, self.target_body.position)
        # target_body.
        self.source.mana -= self.mana_usage * dt
        return True

    def finish_cast(self):
        if self.target_body is None:
            return False
        return True

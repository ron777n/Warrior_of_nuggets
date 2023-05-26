import pygame

from .base import Effect
from .bodies import Solid


class NoGravity(Effect):
    timeout = 1000

    def __init__(self):
        super().__init__()

    def effect(self, body, dt):
        if self.timer.has_expired():
            return False
        body.hit_global(-body.space.gravity * body.mass * dt, body.position)
        return True


class FollowEffect(Effect):
    timeout = -1

    def __init__(self, power=10, target=pygame.Rect):
        super().__init__()
        self.target = target
        self.power = power

    def effect(self, body: 'Solid', dt):
        if self.timer.has_expired():
            return False
        body.hit_global((self.target.center - body.position).scale_to_length(self.power) * dt - body.space.gravity * body.mass * dt, body.position)
        return True
        # diff = self.target.center - body.position
        # body.hit_global(diff, )

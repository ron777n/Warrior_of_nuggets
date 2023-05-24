# from physics.objects import Solid
import pygame

from Utils.Timers import Timer
# from .bodies import Solid


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

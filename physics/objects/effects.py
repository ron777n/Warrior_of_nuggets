# from physics.objects import Solid
from Utils.Timers import Timer
# from .bodies import Solid


class Effect:
    timeout: 1000

    def __init__(self, *function, timeout=None):
        self.functions = function
        if timeout is None:
            self.timer = Timer(self.timeout)
        else:
            self.timer = Timer(timeout)

    def effect(self, body, dt):
        if self.timer.has_expired():
            return False
        for function in self.functions:
            function(body, dt)
        return True

    def __add__(self, other: 'Effect') -> 'Effect':
        timeout = min(self.timeout, other.timeout)
        return Effect(self.effect, other.effect, timeout=timeout)

    def __hash__(self):
        return hash(self.functions)

    def __eq__(self, other: 'Effect'):
        return self.functions == other.functions


class NoGravity(Effect):
    timeout = 1000

    def __init__(self):
        super().__init__(self.function)

    @staticmethod
    def function(body: 'Solid', dt):
        body.hit_global(-body.space.gravity * body.mass * dt, body.position)


from Utils.Timers import Timer
# from .bodies import Solid


class Effect:
    timeout: 1000

    def __init__(self, function, timeout=None):
        self.function = function
        if timeout is None:
            self.timer = Timer(self.timeout)
        else:
            self.timer = Timer(timeout)

    def effect(self, body):
        if self.timer.has_expired():
            return False
        self.function(body)
        return True

    def __add__(self, other: 'Effect') -> 'Effect':
        timeout = min(self.timeout, other.timeout)
        return Effect((lambda b: (self.effect(b), other.effect(b))), timeout)


class NoGravity(Effect):
    timeout = 1000

    def __init__(self):
        super().__init__(self.function)

    def function(self, body):
        body.hit_global((0, -20*body.mass), body.position)


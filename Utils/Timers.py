import pygame.time


class Timer:

    def __init__(self, timeout):
        self.timeout = timeout
        self.specifics = {None: pygame.time.get_ticks()}

    def has_expired(self, specific=None):
        return (pygame.time.get_ticks() - self.specifics[specific]) \
            > self.timeout

    def rest(self, specific=None):
        self.specifics[specific] = pygame.time.get_ticks()


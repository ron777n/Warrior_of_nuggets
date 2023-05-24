import pygame


class Timer:

    def __init__(self, timeout, specifics=(None,)):
        self.timeout = timeout
        self.specifics = {specific: pygame.time.get_ticks() for specific in specifics}

    def has_expired(self, specific=None) -> bool:
        if self.timeout < 0:
            return False
        return (pygame.time.get_ticks() - self.specifics.get(specific, -self.timeout)) \
            > self.timeout

    def reset(self, specific=None):
        self.specifics[specific] = pygame.time.get_ticks()


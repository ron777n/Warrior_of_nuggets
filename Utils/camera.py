from typing import Optional

import pygame
import pymunk

from physics.objects import BaseObject
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.trackers import BoundTracker


class Camera:

    def __init__(self, background: pygame.Surface, *objects):
        self.background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.target = None
        self.items: list[BaseObject] = []
        self.tracker: Optional[BoundTracker] = None

    def display(self):
        self.display_surface.blit(self.background, (0, 0))
        for item in self.items:
            if self.tracker is not None:
                a, b = item.rect.topleft, self.tracker.rect.topleft
                offset_pos = a[0] - b[0], a[1] - b[1]
            else:
                offset_pos = item.rect.topleft
            self.display_surface.blit(item.image, offset_pos)

    def update(self):
        if self.tracker is not None:
            self.tracker.snap()

    def clear(self, space: Optional[pymunk.Space] = None):
        if space is not None:
            for item in self.items:
                space.remove(item, item.shape)
        self.items.clear()

    def append(self, *items):
        for item in items:
            self.items.append(item)



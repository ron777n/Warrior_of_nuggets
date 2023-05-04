from typing import Optional

import pygame
import pymunk

from physics.objects import BaseObject
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.trackers import BoundTracker


class Camera:
    def __init__(self, background: pygame.Surface, cam_size: tuple[int, int], *objects):
        self.background = background
        self.display_surface = pygame.display.get_surface()
        self.items: list[BaseObject] = []
        self.tracker: Optional[BoundTracker] = None
        self.initial_cam_size = pygame.Vector2(cam_size)
        self.cam_size = pygame.Vector2(cam_size)
        self.target = pygame.Vector2(cam_size)
        self.inital_time = 0

    def display(self):
        img = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_surface.blit(img, (0, 0))

    def update(self):
        if self.inital_time:
            difference = (pygame.time.get_ticks() - self.inital_time) / 1000
            if difference >= 1:
                self.inital_time = 0
            else:
                self.cam_size = self.initial_cam_size.lerp(self.target, difference)
        self.tracker.rect.size = self.cam_size
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

    @property
    def image(self) -> pygame.Surface:
        img = pygame.Surface(self.cam_size)
        img.blit(pygame.transform.scale(self.background, self.cam_size), (0, 0))
        for item in self.items:
            if self.tracker is not None:
                a, b = item.rect.topleft, self.tracker.rect.topleft
                offset_pos = a[0] - b[0], a[1] - b[1]
            else:
                offset_pos = item.rect.topleft
            img.blit(item.image, offset_pos)
        return img

    def zoom(self, value):
        self.target = self.target[0] / value, self.target[1] / value
        self.inital_time = pygame.time.get_ticks()
        self.initial_cam_size = self.cam_size



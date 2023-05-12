from typing import Optional, Union

import pygame
import pymunk

from physics.objects import BaseObject
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.trackers import Tracker


class Camera:
    def __init__(self, background: tuple[str, pygame.Surface],
                 cam_size: tuple[int, int], target: Optional[Union[Tracker, pygame.Rect]] = None):
        mode = background[0]
        if mode in ("static", "repeat"):
            self.background_mode = mode
        else:
            self.background_mode = "static"
        self.background = background[1]
        self.background_size = self.background.get_size()

        self.display_surface = pygame.display.get_surface()
        self.items: list[BaseObject] = []
        if isinstance(target, pygame.Rect):
            target = Tracker(target)
        self.tracker: Optional[Tracker] = target

        self.original_cam_size = pygame.Vector2(cam_size)
        self.initial_cam_size = pygame.Vector2(cam_size)
        self.cam_size = pygame.Vector2(cam_size)
        self.target = pygame.Vector2(cam_size)
        self.initial_time = 0

    def display(self):
        img = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display_surface.blit(img, (0, 0))

    def update(self):
        if self.initial_time:
            difference = (pygame.time.get_ticks() - self.initial_time) / 1000
            if difference >= 1:
                self.initial_time = 0
            else:
                self.cam_size = self.initial_cam_size.lerp(self.target, difference)
        if self.tracker is not None:
            self.tracker.rect.size = self.cam_size
            self.tracker.snap()

    def clear(self, space: Optional[pymunk.Space] = None):
        if space is not None:
            for item in self.items:
                if isinstance(item, pymunk.Body):
                    space.remove(item, item.shape)
        self.items.clear()

    def remove(self, item: BaseObject):
        if item in self.items:
            self.items.remove(item)

    def append(self, *items: BaseObject):
        for item in items:
            self.items.append(item)

    @property
    def image(self) -> pygame.Surface:
        img = pygame.Surface(self.cam_size)
        if self.background_mode == "static":
            img.blit(pygame.transform.scale(self.background, self.cam_size), (0, 0))
        elif self.background_mode == "repeat":
            left, up = self.tracker.rect.topleft
            for row in range(-(up % self.background_size[1]), int(self.cam_size[1]), self.background_size[1]):
                for col in range(-(left % self.background_size[0]), int(self.cam_size[0]), self.background_size[0]):
                    img.blit(self.background, (col, row))

        for item in self.items:
            if self.tracker is not None:
                a, b = item.rect.topleft, self.tracker.rect.topleft
                offset_pos = a[0] - b[0], a[1] - b[1]
            else:
                offset_pos = item.rect.topleft
            img.blit(item.image, offset_pos)
        red = pygame.Surface((64, 64))
        red.fill("red")
        # print(self.tracker.rect)
        img.blit(red, self.tracker.rect)
        return img

    def zoom(self, value):
        self.target = self.target[0] / value, self.target[1] / value
        self.initial_time = pygame.time.get_ticks()
        self.initial_cam_size = self.cam_size

    def get_mouse_pos(self, pos, global_pos=False) -> tuple[float, float]:
        x, y = pos
        offset_x, offset_y = self.tracker.rect.topleft
        x = (offset_x if global_pos else 0) + x * (self.cam_size[0] / self.original_cam_size[0])
        y = (offset_y if global_pos else 0) + y * (self.cam_size[1] / self.original_cam_size[1])
        return x, y



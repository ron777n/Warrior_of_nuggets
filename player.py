from typing import Optional

import pygame
import pymunk

from physics.objects import Solid
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.camera import Camera
from Utils.trackers import BoundTracker, Tracker


class Player(Solid):
    def __init__(self, space, pos, *, camera: Optional[Camera] = None):
        self.image_ = pygame.transform.scale(pygame.image.load("sprites/Player/Player.png"), (100, 200))
        rect: pygame.Rect = pygame.Rect(pos, (100, 180))
        super().__init__(space, rect, mass=10, body_type="DYNAMIC")
        self.position = pymunk.vec2d.Vec2d(self.rect.centerx, self.rect.top)
        print(pos, self.position)

        self.jump = False
        self.moving = 0
        # self.velocity_func = self.velocity_function
        self.position_func = self.position_function
        if camera is not None:
            camera.tracker = Tracker(self._rect, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    @staticmethod
    def position_function(body, dt):
        pymunk.Body.update_position(body, dt)
        body.angle = 0
        body.angular_velocity = 0.0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.moving = 1
            elif event.key == pygame.K_a:
                self.moving = -1
            elif event.key == pygame.K_SPACE:
                self.apply_impulse_at_local_point((0, -self.mass * self.velocity.y - self.mass * 40), (0, 0))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.moving == 1:
                self.moving = 0
            elif event.key == pygame.K_a and self.moving == -1:
                self.moving = 0

    def update(self):
        if self.moving:
            self.apply_impulse_at_local_point((-self.mass * self.velocity.x + self.mass * self.moving * 17, 0), (0, 0))

    @property
    def image(self):
        self._rect.center = self.position
        return self.image_.copy()

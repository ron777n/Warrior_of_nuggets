from typing import Optional

import pygame
import pymunk

from physics.objects import Solid
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.camera import Camera
from Utils.Timers import Timer
from Utils.trackers import Tracker


class Player(Solid):
    PLAYER_SPEED = 17
    DASH_COOL_DOWN = 700
    DOUBLE_PRESS_COOL_DOWN = 200
    DASH_POWER = 5

    def __init__(self, space, pos, *, camera: Optional[Camera] = None):
        self.image_ = pygame.transform.scale(pygame.image.load("sprites/Player/Player.png"), (100, 200))
        rect: pygame.Rect = pygame.Rect(pos, (100, 180))
        super().__init__(space, rect, mass=10, body_type="DYNAMIC")
        self.position = pymunk.vec2d.Vec2d(self.rect.centerx, self.rect.top)

        self.jump = False
        self.moving = 0
        self.double_tap_timer = Timer(self.DOUBLE_PRESS_COOL_DOWN, ("d", "a"))
        self.dash_timer = Timer(self.DASH_COOL_DOWN)
        self.velocity_func = self.velocity_function
        self.position_func = self.position_function

        if camera is not None:
            camera.tracker = Tracker(self._rect, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    @staticmethod
    def velocity_function(body: 'Player', gravity, damping, dt):
        if not body.dash_timer.has_expired():
            gravity = (0, 0)
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        body.angular_velocity = 0.0

    @staticmethod
    def position_function(body, dt):
        pymunk.Body.update_position(body, dt)
        body.angle = 0
        body.angular_velocity = 0.0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.moving = 1
                if not self.double_tap_timer.has_expired('d'):
                    self.dash()
                self.double_tap_timer.reset('d')
            elif event.key == pygame.K_a:
                self.moving = -1
                if not self.double_tap_timer.has_expired('a'):
                    self.dash()
                self.double_tap_timer.reset('a')
            elif event.key == pygame.K_SPACE:
                self.set_speed((None, -40))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.moving == 1:
                self.moving = 0
            elif event.key == pygame.K_a and self.moving == -1:
                self.moving = 0

    def set_speed(self, speed: tuple[Optional[int], Optional[int]]):
        if speed[0] is not None:
            self.apply_impulse_at_local_point((-self.mass * self.velocity.x + self.mass * speed[0], 0), (0, 0))
        if speed[1] is not None:
            self.apply_impulse_at_local_point((0, -self.mass * self.velocity.y + self.mass * speed[1]), (0, 0))

    def dash(self):
        self.dash_timer.reset()
        self.set_speed((self.moving * self.PLAYER_SPEED * self.DASH_POWER, None))
        self.moving = 0

    def update(self):
        if self.moving:
            self.set_speed((self.moving * self.PLAYER_SPEED, None))

    @property
    def image(self) -> pygame.Surface:
        self._rect.center = self.position
        img = self.image_.copy()
        return img

from typing import Optional

import pygame
import pymunk

from .Inventory import *
from my_events import PLAYER_DIED_EVENT
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
    BASE_HEALTH = 100

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
        self.health = self.BASE_HEALTH

        # camera
        self.camera = camera
        if camera is not None:
            camera.tracker = Tracker(self._rect, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.looking_angle = 0

        # inventory
        self.inventory_active = False
        self.inventory = Inventory()
        self.inventory.add_item(ShotGun(self.space, self.camera, self))
        self.inventory.add_item(ShotGun(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))
        self.inventory.add_item(Knife(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))

    @staticmethod
    def velocity_function(body: 'Player', gravity, damping, dt):
        if not body.dash_timer.has_expired():
            gravity = (0, 0)
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        body.angular_velocity = 0.0

    @staticmethod
    def position_function(body: 'Player', dt):
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
            elif event.key == pygame.K_TAB:
                self.inventory_active = not self.inventory_active
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.moving == 1:
                self.moving = 0
            elif event.key == pygame.K_a and self.moving == -1:
                self.moving = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.inventory.use_selected_item(self.rect.center,
                                             self.camera.get_mouse_pos(event.pos, True),
                                             event.button,
                                             True)

    def set_speed(self, speed: tuple[Optional[int], Optional[int]]):
        if speed[0] is not None:
            self.apply_impulse_at_local_point((-self.mass * self.velocity.x + self.mass * speed[0], 0), (0, 0), True)
        if speed[1] is not None:
            self.apply_impulse_at_local_point((0, -self.mass * self.velocity.y + self.mass * speed[1]), (0, 0), True)

    def dash(self):
        self.dash_timer.reset()
        self.set_speed((self.moving * self.PLAYER_SPEED * self.DASH_POWER, None))
        self.moving = 0

    def update(self):
        if self.camera:
            mouse_pos = pymunk.Vec2d(*self.camera.get_mouse_pos())
            diff_vector = mouse_pos - (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.looking_angle = -int(diff_vector.angle_degrees)
        if self.moving:
            self.set_speed((self.moving * self.PLAYER_SPEED, None))

    @property
    def image(self) -> pygame.Surface:
        self._rect.center = self.position
        img = self.image_.copy()
        return img

    def apply_impulse_at_local_point(self, impulse, point=(0, 0), inside=False):
        super().apply_impulse_at_local_point(impulse, point)
        if inside:
            return
        power = abs(pymunk.Vec2d(*impulse))
        if power > 1000:
            self.damage(power / 1000)

    def damage(self, amount):
        self.health -= amount
        print(self.health)
        if self.health <= 0:
            pygame.event.post(pygame.event.Event(PLAYER_DIED_EVENT))

    def heal(self, amount):
        self.health = min(self.BASE_HEALTH, self.health + amount)
        print(self.health)

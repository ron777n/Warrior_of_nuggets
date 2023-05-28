from typing import Optional

import pygame
import pymunk

from physics.Magic import Magic, PushMagic
from physics.Magic.MagicTypes import HoldMagic
from physics.objects.effects import FollowEffect, NoGravity
from .Inventory import *
from CONSTANTS import PLAYER_DIED_EVENT
from physics.objects import ray_trace_first, Solid
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils.camera import Camera
from Utils.Timers import Timer
from Utils.trackers import Tracker


def player_body() -> pymunk.Shape:
    shape: pygame.Poly = pymunk.Poly.create_box(None, (100, 180))
    shape.mass = 100
    shape.friction = 0.7
    return shape


class PlayerHand:
    def __init__(self, left):
        self.base_image = pygame.image.load("sprites/Player/Hand" + ("Left" if left else "Right") + ".png")

    def get_display(self, angle_vector) -> tuple[pygame.Rect, pygame.Surface]:
        img = self.base_image.copy()
        img = pygame.transform.rotate(img, -angle_vector.angle_degrees)
        # if abs(angle_vector.angle_degrees) > 90:
        #     img = pygame.transform.flip(img, True, True)
        rect = img.get_rect()
        return rect, img


class Player(Solid):
    PLAYER_SPEED = 20
    DASH_COOL_DOWN = 700
    DOUBLE_PRESS_COOL_DOWN = 200
    DASH_POWER = 5
    BASE_HEALTH = 100
    MANA_REGEN_COOL_DOWN = 500
    HEALTH_REGEN_COOL_DOWN = 1000

    unlocked_magics: dict[str, Magic] = {}

    base_mana = 100

    def __init__(self, space, pos, *, camera: Camera):
        super().__init__(space, pos, player_body(), body_type_name="DYNAMIC", image_path="sprites/Player/Player.png")
        self.hand_left = PlayerHand(True)
        self.hand_right = PlayerHand(True)

        # timers:
        self.double_tap_timer = Timer(self.DOUBLE_PRESS_COOL_DOWN, ("d", "a"))
        self.mana_regen_timer = Timer(self.MANA_REGEN_COOL_DOWN)
        self.health_regen_timer = Timer(self.HEALTH_REGEN_COOL_DOWN)

        # movement
        self.jump = False
        self.moving = 0
        self.dash_timer = Timer(self.DASH_COOL_DOWN)
        self.velocity_func = self.velocity_function
        self.position_func = self.position_function

        # camera
        self._rect = self.rect
        self.camera = camera
        camera.tracker = Tracker(self._rect, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.looking_angle = 0
        self.camera.append(self)

        # Player Data
        self.health = self.BASE_HEALTH
        self.unlocked_magics['f'] = PushMagic(self)
        self.unlocked_magics['e'] = HoldMagic(self, self.camera.global_mouse_rect)
        self.active_magics: set[Magic] = set()

        # inventory
        self.inventory_active = False
        self.inventory = Inventory()
        self.inventory.add_item(ShotGun(self.space, self.camera, self))
        self.inventory.add_item(ShotGun(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))
        self.inventory.add_item(Knife(self.space, self.camera, self))
        self.inventory.add_item(Nugget(self.space, self.camera, self))

    @property
    def image(self):
        img = super().image
        pos = pymunk.Vec2d(*self.camera.get_mouse_pos(mid=True))
        pos += 0, 60
        right_rect, right_image = self.hand_right.get_display(pos.normalized())
        left_rect, left_image = self.hand_left.get_display(pos.normalized())
        if abs(pos.angle_degrees) > 90:
            img = pygame.transform.flip(img, True, False)
            img.blit(left_image, (self.rect.width / 2 - 10 - left_rect.width, 40))
            img.blit(right_image, (self.rect.width / 2 + 10, 40))
        else:
            img.blit(right_image, (self.rect.width / 2 + 10, 40))
            img.blit(left_image, (self.rect.width / 2 - 10 - left_rect.width, 40))
        return img

    @staticmethod
    def velocity_function(body: 'Player', gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        body.angular_velocity = 0.0

    @staticmethod
    def position_function(body: 'Player', dt):
        pymunk.Body.update_position(body, dt)
        body.angle = 0

    def try_use_magic(self, key, finish=False):
        target_magic = self.unlocked_magics.get(key)
        if not target_magic:
            return
        if finish:
            if target_magic.finish_cast():
                self.active_magics.remove(target_magic)
        else:
            if target_magic.cast():
                self.active_magics.add(target_magic)

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
            else:
                self.try_use_magic(event.unicode)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.moving == 1:
                self.moving = 0
            elif event.key == pygame.K_a and self.moving == -1:
                self.moving = 0
            else:
                self.try_use_magic(event.unicode, True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.inventory.use_selected_item(self.rect.center,
                                             self.camera.get_mouse_pos(global_pos=True),
                                             event.button,
                                             True)

    def set_speed(self, speed: tuple[Optional[int], Optional[int]]):
        if speed[0] is not None:
            self.hit_local((-self.mass * self.velocity.x + self.mass * speed[0], 0), (0, 0), False)
        if speed[1] is not None:
            self.hit_local((0, -self.mass * self.velocity.y + self.mass * speed[1]), (0, 0), False)

    def dash(self):
        self.dash_timer.reset()
        self.add_effect(NoGravity())
        self.set_speed((self.moving * self.PLAYER_SPEED * self.DASH_POWER, None))
        self.moving = 0

    def update(self, dt):
        super().update(dt)
        if self.camera:
            self._rect.update(self.rect)
            mouse_pos = pymunk.Vec2d(*self.camera.get_mouse_pos())
            diff_vector = mouse_pos - (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.looking_angle = -int(diff_vector.angle_degrees)
        if self.moving:
            self.set_speed((self.moving * self.PLAYER_SPEED, None))
        if self.health_regen_timer.has_expired():
            self.health += 10 * dt
        if self.mana_regen_timer.has_expired():
            self.mana += 10 * dt
        for magic in self.active_magics:
            if not magic.update(dt):
                self.active_magics.remove(magic)

    def damage_local(self, amount, location_=(0, 0)):
        self.health -= amount
        self.health_regen_timer.reset()

    @property
    def health(self):
        if self._health <= 0:
            pygame.event.post(pygame.event.Event(PLAYER_DIED_EVENT))
        return int(self._health)

    @health.setter
    def health(self, value):
        self._health = min(self.BASE_HEALTH, value)

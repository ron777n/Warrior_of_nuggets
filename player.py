import pygame
import pymunk

from physics.objects import Solid


class Player(Solid):
    def __init__(self, space, pos, *, target=None):
        self.image_ = pygame.transform.scale(pygame.image.load("sprites/Player/Player.png"), (100, 200))
        rect: pygame.Rect = pygame.Rect(pos, (100, 200))
        super().__init__(space, rect, mass=10, body_type=pymunk.Body.DYNAMIC)

        self.jump = False
        self.moving = 0
        self.velocity_func = self.velocity_function

    @staticmethod
    def velocity_function(body: 'Player', gravity, damping, delta_time):
        pymunk.Body.update_velocity(body, gravity, damping, delta_time)
        vel = body.velocity
        if body.moving:
            vel = body.moving * 30, vel[1]
        if body.jump:
            vel = vel[0], -30
            body.jump = False
        body.velocity = vel

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.moving = 1
            elif event.key == pygame.K_a:
                self.moving = -1
            elif event.key == pygame.K_SPACE:
                self.jump = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.moving == 1:
                self.moving = 0
            elif event.key == pygame.K_a and self.moving == -1:
                self.moving = 0

    @property
    def image(self):
        self._rect.center = self.position
        return self.image_.copy()
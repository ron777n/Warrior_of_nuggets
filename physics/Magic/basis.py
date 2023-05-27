import abc
from typing import Optional, Type

import pygame
import pymunk

from physics.objects import Solid
from Utils.Timers import Timer


class Magic(abc.ABC):
    combination_rules: dict[frozenset, Type['Magic']] = {}
    name: str
    icon: pygame.Surface
    description: str
    image: pygame.Surface
    direction: pymunk.Vec2d = pymunk.Vec2d.zero()
    mana_usage: float = 1
    base_cool_down: int = 0

    def __init__(self, source: Solid):
        self.source = source
        self.cool_down_timer = Timer(self.base_cool_down) if self.base_cool_down else None

    def cast(self) -> bool:
        # Implement the logic for casting the magic
        if self.source.mana < self.mana_usage:
            return False
        if self.cool_down_timer is not None and self.cool_down_timer.has_expired():
            return False
        return True

    def _mana_diff(self, other: 'Solid', aura=False):
        mana_diff = self.source.mana / other.mana
        if aura:
            mana_diff /= abs(self.source.position - other.position)
        return mana_diff

    def update(self, dt: int):
        # Implement any update logic for the magic (e.g., cooldowns, duration)
        pass

    def __add__(self, other) -> 'Magic':
        if not isinstance(other, Magic):
            raise TypeError("Cannot combine with a non magic object")

        new_magic_type = self.combine_with(self, other)
        if new_magic_type is not None:
            return new_magic_type
        self.combine_effects(other)

    @staticmethod
    def combine_with(self, other) -> Optional['Magic']:
        combination_key = frozenset({type(self), type(other)})
        return self.combination_rules.get(combination_key, None)

    def combine_effects(self, other):
        pass

    def finish_cast(self):
        pass


import math
from typing import Optional, Union

import pygame
import pymunk

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils import Gui
from Utils.camera import Camera
from Utils.Gui import BaseGui


class Item:
    image: pygame.Surface

    def __init__(self, space: pymunk.Space, camera, owner):
        self.space = space
        self.camera: Camera = camera
        self.owner = owner
        self.hand_vec = pymunk.Vec2d(1, 1)

    def use_item(self, start_pos, use_vector, button: int, down: bool) -> bool:
        """
        Uses the item

        use_vector: is the vector of how to use the item,
        meaning it creates a line from where the player is to where to use it

        use_type: is the buttons of the use, middle click right click etc, and whether it's a down click or an up click
        """
        pass

    def add_to_item(self, item) -> bool:
        pass


class Bag(BaseGui):
    bag_count = 64
    tile_image = pygame.image.load("sprites/Gui/Inventory/ItemSlot.png")

    def __init__(self, rect):
        self.rect = rect.copy()
        self.items: list[Optional[Item]] = [None] * self.bag_count
        # size^2 = (width * height)/bag_count
        self.bag_tile_size = math.sqrt(self.rect.size[0] * self.rect.size[1] / self.bag_count)
        (col, margin_x), (row, margin_y) = (divmod(self.rect.size[0] / self.bag_tile_size, 1),
                                            divmod(self.rect.size[1] / self.bag_tile_size, 1))
        self.margin = margin_x, margin_y
        self.bag_row_count = col
        self.bag_col_count = row
        self.tile_image = pygame.transform.scale(self.tile_image, (self.bag_tile_size, self.bag_tile_size))
        self.holding: Optional[Item] = None

    def add_item(self, item_to_add: Item):
        for i, item in enumerate(self.items):
            if item is None:
                self.items[i] = item_to_add
                return True
            if type(item) == type(item_to_add) and item.add_to_item(item_to_add):
                return True
        return False

    @property
    def image(self):
        img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        for i, item in enumerate(self.items):
            tile_pos = (i % self.bag_col_count) * self.bag_tile_size, (i // self.bag_row_count) * self.bag_tile_size
            tile_image = self.tile_image.copy()
            if item is None:
                img.blit(tile_image, tile_pos)
                continue
            tile_image.blit(pygame.transform.scale(item.image, (self.bag_tile_size, self.bag_tile_size)), (0, 0))
            img.blit(tile_image, tile_pos)
        return img

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        if not self.collide_point(location):
            if button_type == pygame.BUTTON_LEFT and not down and self.holding is not None:
                self.add_item(self.holding)
                self.holding = None
            return False
        if button_type != pygame.BUTTON_LEFT:
            return False
        location = (location[0] - self.rect.left) // self.bag_tile_size, \
                   (location[1] - self.rect.top) // self.bag_tile_size
        index = int(location[0] + location[1] * self.bag_col_count)
        if down:
            self.holding = self.items[index]
            self.items[index] = None
        elif self.holding is not None:
            if self.items[index] is None:
                self.items[index] = self.holding
                self.holding = None
            else:
                self.add_item(self.holding)
                self.holding = None
        return True


class Inventory(Gui.Menu):
    background_image = pygame.image.load("sprites/Gui/Inventory/background.png")

    def __init__(self, _player):
        screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
        inventory_size = self.background_image.get_size()
        self.box_size = inventory_size
        self.rect = pygame.Rect(screen_size[0] // 4, screen_size[1] // 4, *inventory_size)
        self.bag = Bag(self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.2))
        self.hand_left = [None] * 3
        self.hand_right = [None] * 3

    def display(self, display_surface: pygame.Surface):
        img = self.background_image.copy()
        img.blit(self.bag.image, (self.bag.rect.left - self.rect.left, self.bag.rect.top - self.rect.top))
        display_surface.blit(img, self.rect)

    def add_item(self, item_to_add: Item) -> bool:
        return self.bag.add_item(item_to_add)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
        holding = self.bag.holding
        if holding is not None:
            print(holding)
        self.bag.click(location, button_type, down)
        return r

    @property
    def selected_item(self):
        return None

    def use_selected_item(self, start_pos, end_pos, button: int, down: bool):
        return
        item = self.selected_item
        if item is not None:
            should_delete = item.use_item(start_pos, end_pos, button, down)
            if should_delete:
                self.bag[self.current_item_index] = None

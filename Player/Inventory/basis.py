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

    def click(self, location: tuple[int, int], button_type: int, down: bool, held_item: Optional[Item] = None) -> \
            Union[bool, Optional[Item]]:
        if not self.collide_point(location):
            return False
        if button_type != pygame.BUTTON_LEFT:
            return False
        location = (location[0] - self.rect.left) // self.bag_tile_size, \
                   (location[1] - self.rect.top) // self.bag_tile_size
        index = int(location[0] + location[1] * self.bag_col_count)
        target_item = self.items[index]
        if down:
            self.items[index] = None
            return target_item
        elif held_item is not None and target_item is None:
            self.items[index] = held_item
            return True
        return False


class HotBar(BaseGui):
    tile_image = pygame.image.load("sprites/Gui/Inventory/ItemSlot.png")

    def __init__(self, rect):
        self.rect = rect.copy()
        self.items: list[list[Optional[Item]]] = [[None] * 3, [None] * 3]
        self.margin = 20
        self.slot_size = (self.rect.width - self.margin) / 6
        self.tile_image = pygame.transform.scale(self.tile_image, (self.slot_size, self.slot_size))

    @property
    def image(self):
        img = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        for i, item in enumerate(self.items[0] + self.items[1]):
            tile_image = self.tile_image.copy()
            if item is not None:
                tile_image.blit(pygame.transform.scale(item.image, (self.slot_size, self.slot_size)), (0, 0))
            if i < 3:
                loc = (i * self.slot_size, 0)
            else:
                loc = (i * self.slot_size + self.margin, 0)
            img.blit(tile_image, loc)
        return img

    def click(self, location: tuple[int, int], button_type: int, down: bool, held_item: Optional[Item] = None) -> \
            Union[bool, Optional[Item]]:
        if not self.collide_point(location):
            return False
        if button_type != pygame.BUTTON_LEFT:
            return False
        index = [0] * 2
        if location[0] - self.rect.left > self.slot_size * 3:
            index[0] = 1
            location = location[0] - self.margin - self.slot_size * 3, location[1]
        else:
            index[0] = 0
        index[1] = int((location[0] - self.rect.left) // self.slot_size)
        if index[1] < 0:
            return False
        target_item = self.items[index[0]][index[1]]
        if down:
            self.items[index[0]][index[1]] = None
            return target_item
        elif target_item is None and held_item is not None:
            self.items[index[0]][index[1]] = held_item
            return True
        return False


class Armor(BaseGui):
    pass


class Inventory(Gui.Menu):
    background_image = pygame.image.load("sprites/Gui/Inventory/background.png")

    def __init__(self, _player):
        screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
        inventory_size = self.background_image.get_size()
        self.box_size = inventory_size
        self.rect = pygame.Rect(screen_size[0] // 4, screen_size[1] // 4, *inventory_size)
        self.bag = Bag(self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.2)
                       .move(0, self.rect.height * 0.1))
        self.hot_bar = HotBar(self.rect.inflate(-self.rect.width * 0.4, -self.rect.height * 0.8)
                              .move(-self.rect.width * 0.2, -self.rect.height * 0.4))
        self.armor = Armor()
        self.held_item: Optional[Item] = None

    def display(self, display_surface: pygame.Surface):
        img = self.background_image.copy()
        img.blit(self.bag.image, (self.bag.rect.left - self.rect.left, self.bag.rect.top - self.rect.top))
        img.blit(self.hot_bar.image, (self.hot_bar.rect.left - self.rect.left, self.hot_bar.rect.top - self.rect.top))
        display_surface.blit(img, self.rect)

    def add_item(self, item_to_add: Item) -> bool:
        return self.bag.add_item(item_to_add)

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
        if button_type == pygame.BUTTON_LEFT:
            hot_bar = self.hot_bar.click(location, button_type, down, self.held_item)
            bag = self.bag.click(location, button_type, down, self.held_item)
            if hot_bar is True or bag is True:
                self.held_item = None
            elif hot_bar is False and bag is False:
                self.bag.add_item(self.held_item)
                self.held_item = None
            elif hot_bar not in (False, None):
                self.held_item = hot_bar
            elif bag not in (False, None):
                self.held_item = bag
        return r

    def use_selected_item(self, hand: bool, start_pos, end_pos, button: int, down: bool):
        item = self.hot_bar.items[hand][0]
        if item is not None:
            should_delete = item.use_item(start_pos, end_pos, button, down)
            if should_delete:
                self.hot_bar.items[hand][0] = None

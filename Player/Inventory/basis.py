import math
from typing import Optional

import pygame
import pymunk

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils import Gui
from Utils.camera import Camera


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


class Inventory(Gui.Menu):
    tile_image = pygame.image.load("sprites/Gui/Inventory/ItemSlot.png")
    background_image = pygame.image.load("sprites/Gui/Inventory/background.png")

    def __init__(self, _player):
        screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
        inventory_size = self.background_image.get_size()
        self.box_size = inventory_size
        self.rect = pygame.Rect(screen_size[0] // 4, screen_size[1] // 4, *inventory_size)
        self.bag_count = 64
        self.bag: list[Optional[Item]] = [None] * self.bag_count
        self.current_item_index = 0
        # size^2 = (width * height)/bag_count
        self.bag_tile_size = math.sqrt(self.box_size[0] * self.box_size[1] / self.bag_count)
        self.bag_row_count = self.box_size[0] / self.bag_tile_size
        self.bag_col_count = self.box_size[1] / self.bag_tile_size
        self.tile_image = pygame.transform.scale(self.tile_image, (self.bag_tile_size, self.bag_tile_size))

        self.hand_left = [None] * 3
        self.hand_right = [None] * 3
        self.holding = None

    def display(self, display_surface: pygame.Surface):
        img = self.background_image.copy()
        for i, item in enumerate(self.bag):
            image_rect = pygame.Rect((i * self.bag_tile_size) % self.box_size[0],
                                     (i * self.bag_tile_size) // self.box_size[1],
                                     self.bag_tile_size, self.bag_tile_size)
            tile_image = self.tile_image.copy()
            print(image_rect, tile_image)
            if item is None:
                img.blit(tile_image, image_rect)
                continue
            tile_image.blit(item.image, image_rect)
            img.blit(tile_image, image_rect)
            # item_img = pygame.transform.scale(item.image, image_rect.size)
        display_surface.blit(img, self.rect)

    def add_item(self, item_to_add: Item) -> bool:
        for i, item in enumerate(self.bag):
            if item is None:
                self.bag[i] = item_to_add
                return True
            if type(item) == type(item_to_add):
                if item.add_to_item(item_to_add):
                    return True
        return False

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
        return r
        inventory_id = (location[0] - self.rect.left) // self.box_size, (location[1] - self.rect.top) // self.box_size
        inventory_id = inventory_id[0] + inventory_id[1] * self.max_items
        if r and button_type == pygame.BUTTON_LEFT:
            if down:
                self.holding = inventory_id
            elif self.items[inventory_id] is None:
                item = self.items[self.holding]
                self.items[self.holding] = None
                self.items[inventory_id] = item
        elif r and button_type == pygame.BUTTON_RIGHT:
            self.current_item_index = inventory_id
        return r

    @property
    def selected_item(self):
        return self.bag[self.current_item_index]

    def use_selected_item(self, start_pos, end_pos, button: int, down: bool):
        item = self.selected_item
        if item is not None:
            should_delete = item.use_item(start_pos, end_pos, button, down)
            if should_delete:
                self.bag[self.current_item_index] = None

import abc
from typing import Optional

import pygame
import pymunk

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from Utils import Gui
from Utils.camera import Camera


class Item:
    image: pygame.Surface

    def __init__(self, space: pymunk.Space, camera):
        self.space = space
        self.camera: Camera = camera

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
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
    def __init__(self):
        screen_size = SCREEN_WIDTH, SCREEN_HEIGHT
        inventory_size = screen_size[0] // 2, screen_size[1] // 2
        self.rect = pygame.Rect(screen_size[0] // 4, screen_size[1] // 4, *inventory_size)
        self.max_items = 8
        self.items: list[Optional[Item]] = [None] * self.max_items * self.max_items
        self.current_item_index = 0
        self.box_size = 64
        self.holding = None

    def display(self, display_surface: pygame.Surface):
        img = pygame.Surface(self.rect.size)
        img.fill("red")
        for i, item in enumerate(self.items):
            if item is None:
                continue
            image_rect = pygame.Rect((i % self.max_items) * self.box_size, (i // self.max_items) * self.box_size,
                                     self.box_size, self.box_size)
            item_img = pygame.transform.scale(item.image, image_rect.size)
            img.blit(item_img, image_rect)
        display_surface.blit(img, self.rect)

    def add_item(self, item_to_add: Item) -> bool:
        for i, item in enumerate(self.items):
            if item is None:
                self.items[i] = item_to_add
                return True
            if type(item) == type(item_to_add):
                if item.add_to_item(item_to_add):
                    return True
        return False

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        r = self.rect.collidepoint(location)
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

    def use_selected_item(self, start_pos, end_pos, button: int, down: bool):
        item = self.items[self.current_item_index]
        if item is not None:
            should_delete = item.use_item(start_pos, end_pos, button, down)
            if should_delete:
                self.items[self.current_item_index] = None

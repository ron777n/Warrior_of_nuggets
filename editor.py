"""
This is for the level creator.
"""
import json
from typing import Union

import pygame

import level
from Menus import EditorMenu
from physics.objects import BaseObject, Solid
from settings import *
from Utils.camera import Camera

with open("settings.json") as f:
    settings = json.load(f)


def create_lines() -> pygame.Surface:
    cols, rows = settings["Screen"]["Size"]

    rows //= settings["Editor"]["TileSize"]
    cols //= settings["Editor"]["TileSize"]
    img = pygame.Surface((TILE_SIZE, TILE_SIZE))
    img.fill("white")
    pygame.draw.rect(img, "black", pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE), 1)

    return img


class Editor:
    """
    The class that holds the loop
    """

    def __init__(self, transition, level_name):
        self.transition = transition
        self.level_name = level_name

        self.selected_block = None
        self.display_surface = pygame.display.get_surface()

        lines = create_lines()
        self.player: tuple[int, int] = (0, 0)

        self.camera_position = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

        self.camera = Camera(("repeat", lines), (SCREEN_WIDTH, SCREEN_HEIGHT), self.camera_position)

        self.canvas_data: dict[tuple[int, int], Union[EditorMenu.EditorTile, str]] = {}

        self.menu = EditorMenu.EditorMenu(
            (self.set_block, self.set_player, self.delete_block, self.start, self.save_level), Solid)
        self.settings = EditorMenu.TileMenu(self.menu.add_button)
        self.load_level()

    def delete_block(self):
        self.selected_block = "delete"

    def set_player(self):
        self.selected_block = "player"

    def start(self):
        self.save_level()
        self.transition()

    def set_block(self, block, block_data):
        self.selected_block = (block, (), block_data)

    def event_loop(self, delta_time):
        """
        handles the Game loop
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            self.handle_event(event)

    def handle_event(self, event: pygame.event):
        """
        handles the event, because
        :param event:
        """
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[1] or (event.buttons[0] and pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.camera_position.centerx -= event.rel[0]
                self.camera_position.centery -= event.rel[1]
            elif event.buttons[0]:
                mouse_data = event.pos, 1, True
                if (self.settings.active and not self.settings.collide_point(event.pos)) or not self.menu.collide_point(
                        event.pos):
                    self.click(*mouse_data)

        elif event.type == pygame.MOUSEWHEEL:
            if event.x:
                self.camera_position.centerx -= event.x * TILE_SIZE / 2
            if event.y:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.camera_position.centerx -= event.y * TILE_SIZE / 2
                else:
                    self.camera_position.centery -= event.y * TILE_SIZE / 2

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_data = event.pos, event.button, True
            if not ((self.settings.active and self.settings.click(*mouse_data)) or self.menu.click(*mouse_data)):
                self.click(*mouse_data)
            self.update_camera()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_data = event.pos, event.button, False
            if (self.settings.active and not self.settings.click(*mouse_data)) or not self.menu.click(*mouse_data):
                self.click(*mouse_data)
            self.update_camera()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start()

    def click(self, location: tuple[int, int], button_type: int, down: bool) -> bool:
        if not down:
            return False
        tile_cords = self.camera.get_mouse_pos(location, True)
        tile_cords = int(tile_cords[0] // TILE_SIZE), int(tile_cords[1] // TILE_SIZE)

        if tile_cords not in self.canvas_data:
            if button_type != pygame.BUTTON_LEFT:
                return False
            if isinstance(self.selected_block, tuple):
                self.canvas_data[tile_cords] = EditorMenu.EditorTile(self.selected_block)
            elif self.selected_block == "player":
                del self.canvas_data[self.player]
                self.player = tile_cords
                self.canvas_data[self.player] = "player"
            self.update_camera()
        elif self.selected_block == "delete" and button_type == pygame.BUTTON_LEFT and \
                self.canvas_data[tile_cords] != "player":
            del self.canvas_data[tile_cords]
            self.update_camera()

        elif button_type == pygame.BUTTON_RIGHT:
            tile = self.canvas_data[tile_cords]
            if self.settings and self.settings.current == tile:
                self.settings.active = False
                self.settings.current = None
            else:
                self.settings.reset(tile)

        return True

    def run(self, dt):
        """
        starts the game loop
        """
        self.camera.update()
        self.camera.display()
        # self.draw()
        self.event_loop(dt)
        self.draw_gui()

    def update_camera(self):
        self.camera.clear()
        for coordinate, tile in self.canvas_data.items():
            dat = BaseObject()
            if isinstance(tile, str):
                if tile == "player":
                    dat.image = pygame.transform.scale(PLAYER_HEAD, (TILE_SIZE, TILE_SIZE))
                    dat.rect = pygame.Rect((coordinate[0] * TILE_SIZE, coordinate[1] * TILE_SIZE),
                                           (TILE_SIZE, TILE_SIZE))
                    self.player = coordinate
                else:
                    continue
            else:
                image = pygame.image.load(tile.main_block[2]["image_path"][0])
                dat.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
                dat.rect = pygame.Rect((coordinate[0] * TILE_SIZE, coordinate[1] * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
            self.camera.append(dat)

    def draw_player(self):
        self.display_surface.blit(pygame.transform.scale(PLAYER_HEAD, (TILE_SIZE, TILE_SIZE)), self.player)

    def draw_gui(self):
        if self.settings.active:
            self.settings.display(self.display_surface)
        else:
            self.menu.display(self.display_surface)

    def save_level(self):
        buttons = self.menu.get_buttons()
        level.save("Levels/Egg.lvl", self.canvas_data, buttons)

    def load_level(self):
        self.canvas_data.clear()
        data = level.load("Levels/Egg.lvl", True)
        self.canvas_data.update(data["Level"])
        self.update_camera()
        for block, button_data in data["Editor"]:
            if block == "Solid":
                class_type = Solid
            else:
                continue
            button_data = {key: val[0] for key, val in button_data.items()}
            self.menu.add_button(class_type, button_data, class_type.base_image)

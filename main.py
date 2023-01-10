"""
Main, but better
"""
import pygame
import json

# from Game import Game
from level_creator import Editor

with open("settings.json") as f:
    settings = json.load(f)


class Main:
    """
    for global variables and stuff
    """

    def __init__(self, ):
        pygame.init()
        cam_shape = tuple(settings["Screen"]["Size"])
        pygame.display.set_mode(cam_shape)
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        cursor_surf = pygame.image.load(settings["Cursor"]["Icon"]).convert_alpha()
        cursor = pygame.Cursor(tuple(settings["Cursor"]["ClickCord"]), cursor_surf)
        pygame.mouse.set_cursor(cursor)

        # self.game = Game()
        self.editor = Editor()

    def run(self):
        """
        runs the main loop.
        """
        while True:
            dt = self.clock.tick(60) / 100
            self.editor.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        print("Good bye")

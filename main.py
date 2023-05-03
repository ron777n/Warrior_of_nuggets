"""
Main, but better
"""
import pygame

from editor import Editor

from settings import *
from game import Game


class Main:
    """
    for global variables and stuff
    """

    def __init__(self, ):
        pygame.init()
        cam_shape = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.display.set_mode(cam_shape)
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        cursor_surf = pygame.image.load(settings["Cursor"]["Icon"]).convert_alpha()
        cursor = pygame.Cursor(tuple(settings["Cursor"]["ClickCord"]), cursor_surf)
        pygame.mouse.set_cursor(cursor)

        self.level = Game("Levels/Egg.lvl")
        self.editor = Editor()

    def run(self):
        """
        runs the main loop.
        """
        while True:
            dt = self.clock.tick(60) / 100
            # self.editor.run(dt)
            self.level.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        print("Good bye")

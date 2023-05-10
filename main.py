"""
Main, but better
"""
import pygame

from editor import Editor

from settings import *
from game import Game
from tkinter.filedialog import asksaveasfilename
import sys

if len(sys.argv) < 2:
    level_name = "Levels/egg.lvl"
elif len(sys.argv) == 2:
    if sys.argv[1] == "pick":
        level_name = asksaveasfilename()
    else:
        level_name = "Levels/egg.lvl"
else:
    print("Invalid Arguments")
    exit()


class Main:
    """
    for global variables and stuff
    """

    def __init__(self, ):
        self.editor_active = True
        pygame.init()
        cam_shape = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.display.set_mode(cam_shape)
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        cursor_surf = pygame.image.load(settings["Cursor"]["Icon"]).convert_alpha()
        cursor = pygame.Cursor(tuple(settings["Cursor"]["ClickCord"]), cursor_surf)
        pygame.mouse.set_cursor(cursor)
        self.level_name = level_name

        self.game = Game(self.transition, self.level_name)
        self.editor = Editor(self.transition, self.level_name)

    def run(self):
        """
        runs the main loop.
        """
        while True:
            dt = self.clock.tick(60) / 100
            if self.editor_active:
                self.editor.run(dt)
            else:
                self.game.run(dt)
            pygame.display.update()

    def transition(self):
        if self.editor_active:
            self.game.reset()
        self.editor_active = not self.editor_active


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt:
        print("Good bye")

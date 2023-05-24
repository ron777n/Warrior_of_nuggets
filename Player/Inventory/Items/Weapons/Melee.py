import pygame

from ...basis import Item


class Knife(Item):
    image = pygame.image.load("sprites/objects/tools/Weapons/Knife.png")

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT:
            pass
        elif button == pygame.BUTTON_RIGHT:
            self.owner.damage_local(20)
        return False

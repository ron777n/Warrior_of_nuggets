import pygame

from ...basis import Item


class Nugget(Item):
    image = pygame.image.load("sprites/objects/tools/food/Nugget.png")

    def __init__(self, space, camera, owner, count=1):
        super().__init__(space, camera, owner)
        self.count = count

    def use_item(self, start_pos, end_pos, button: int, down: bool) -> bool:
        if button == pygame.BUTTON_LEFT and down:
            print("EAT NUGGET")
            self.owner.health += 30
            self.count -= 1
            if not self.count:
                return True
        return False

    def add_to_item(self, item) -> bool:
        self.count += 1
        return True

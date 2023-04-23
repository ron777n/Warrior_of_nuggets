import pygame


def tint_image(image: pygame.Surface, color=(0, 0, 0), strength=127) -> pygame.Surface:
    image = image.copy()
    strength /= 255
    image.fill((color[0]*strength, color[1]*strength, color[2]*strength), None, pygame.BLEND_RGBA_ADD)
    # image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image

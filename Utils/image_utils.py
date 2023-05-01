import textwrap

import pygame


class Text(pygame.Surface):
    """
    simple text with no background image
    """

    def __init__(self, text: str, color=(0, 0, 0), font=None):
        font = self.create_font(font)
        self.text_color = color
        self.font = font
        self.text = text if isinstance(text, str) else ("" if text is None else str(text))
        self.lines = self.text.split("\n")
        font_size = self.font.size(max(self.lines, key=lambda x: self.font.size(x)[0]))
        self.size = font_size[0], font_size[1] * len(self.lines)
        super().__init__(self.size, pygame.SRCALPHA)
        for i, line in enumerate(self.lines):
            rect = self.get_rect()
            rect.top = font_size[1] * i
            self.blit(self.font.render(line, True, self.text_color), rect)

    @staticmethod
    def create_font(font):
        if font is None:
            font = pygame.font.SysFont('Comic Sans MS', 20)
        elif isinstance(font, int):
            font = pygame.font.SysFont('Comic Sans MS', font)
        assert isinstance(font, pygame.font.Font), "invalid font type"
        return font

    def draw(self, surface: pygame.Surface, mode=("center",)):
        """
        draws the text on a surface.
        if mode is "center" then no additional arguments are required
        if "left", "right", "up" or "down"(ima add more later) then a buffer of the corner is required as the second
        tuple element
        """
        if mode[0] == "center":
            surface.blit(self, self.get_rect(center=(surface.get_width() / 2, surface.get_height() / 2)))
        elif mode[0] == "left":
            surface.blit(self, self.get_rect(midleft=(mode[1], surface.get_height() / 2)))
        elif mode[0] == "top_left":
            surface.blit(self, self.get_rect(midleft=(mode[1], mode[2])))

    def wrap(self, size: tuple[int, int]) -> 'Text':
        """
        returns a new text containing the same text and color with different font size(not yet) or new lines
        :param size:
        """
        new_text = ""
        if self.size[0] > size[0]:
            for line in self.lines:
                line_size = self.font.size(line)[0]
                if line_size > size[0]:
                    line = textwrap.fill(line, size[0] // 10)
                new_text += line
        else:
            return self
        return Text(new_text, self.text_color, self.font)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'Text<{self.text},{self.text_color},F{self.font}>{self.size}'


def tint_image(image: pygame.Surface, color=(0, 0, 0), strength=127) -> pygame.Surface:
    image = image.copy()
    strength /= 255
    image.fill((color[0] * strength, color[1] * strength, color[2] * strength), None, pygame.BLEND_RGBA_ADD)
    # image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image

import pygame


class Tracker:
    """
    this object does not "follow" its target but it lets you get things like the distance between itself and its target
    or the angle
    """

    def __init__(self, target: pygame.rect.Rect, tracker_rect: pygame.Rect = pygame.Rect(0, 0, 50, 50)):
        self.target: pygame.rect.Rect = target
        self.rect = tracker_rect

    def snap(self):
        """
        snaps itself to its target
        :return:
        """
        self.rect.center = self.target.center


class BoundTracker(Tracker):
    """
    tracker stays inside its boundaries, if snapped
    """

    def __init__(self, boundaries, target: pygame.Rect, tracker_rect=pygame.Rect(0, 0, 50, 50)):
        super().__init__(target, tracker_rect)
        self.offset = pygame.math.Vector2()
        self.boundaries = boundaries
        self.half_w = self.rect.width / 2
        self.half_h = self.rect.height / 2

    def snap(self):
        """
        centers the camera to an object
        """
        self.offset.x = min(self.target.centerx, self.boundaries[0] - self.half_w) - self.half_w
        self.offset.x = max(self.offset.x, 0)
        self.offset.y = min(self.target.centery, self.boundaries[1] - self.half_h) - self.half_h
        self.offset.y = max(self.offset.y, 0)
        self.rect.topleft = tuple(self.offset)

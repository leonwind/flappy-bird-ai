import pygame


class Border:
    VELOCITY = 5

    def __init__(self, border_img: pygame.Surface, pos_y):
        self.start = 0
        self.end = border_img.get_width()
        self.pos_y = pos_y

    def move(self):
        pass

    def draw(self):
        pass
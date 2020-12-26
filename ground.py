import pygame


class Ground:
    VELOCITY = 5

    def __init__(self, pos_y, ground_img: pygame.Surface):
        self.start = 0
        self.end = ground_img.get_width()
        self.pos_y = pos_y

        self.ground_img = ground_img

    def move(self):
        pass

    def draw(self, window: pygame.Surface):
        window.blit(self.ground_img, (0, self.pos_y))
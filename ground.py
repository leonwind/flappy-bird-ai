import pygame
from bird import Bird


class Ground:
    VELOCITY = 5

    def __init__(self, pos_y, ground_img: pygame.Surface):
        self.start = 0
        self.end = ground_img.get_width()
        self.pos_y = pos_y

        self.ground_img: pygame.Surface = ground_img

    def is_colliding(self, bird: Bird) -> bool:
        bird_mask = bird.get_mask()
        ground_mask = pygame.mask.from_surface(self.ground_img)

        offset = (bird.pos_x, round(bird.pos_y - self.pos_y))

        is_overlapping = ground_mask.overlap(bird_mask, offset)
        return is_overlapping

    def move(self):
        pass

    def draw(self, window: pygame.Surface):
        window.blit(self.ground_img, (0, self.pos_y))
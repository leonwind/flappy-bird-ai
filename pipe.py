import random
import pygame
from bird import Bird


class Pipe:
    SPACE = 200
    VELOCITY = 5

    def __init__(self, pos_x, pipe_img):
        self.pos_x = pos_x

        self.bottom_img: pygame.Surface = pipe_img
        self.top_img: pygame.Surface = pygame.transform.flip(pipe_img, False, True)

        height = random.randrange(50, 450)
        self.bottom_y = height + self.SPACE
        self.top_y = height - self.top_img.get_height()

        self.passed = False

    def is_colliding(self, bird: Bird) -> bool:
        """
        Check for pixel perfect collision between the bird  
        and the pipes using masks
        """
        bird_mask = bird.get_mask()
        bottom_pipe_mask = pygame.mask.from_surface(self.bottom_img)
        top_pipe_mask = pygame.mask.from_surface(self.top_img)

        bottom_offset = (self.pos_x - bird.pos_x, round(self.bottom_y - bird.pos_y))
        top_offset = (self.pos_x - bird.pos_x, round(self.top_y - bird.pos_y))

        is_bottom_overlapping = bird_mask.overlap(bottom_pipe_mask, bottom_offset)
        is_top_overlapping = bird_mask.overlap(top_pipe_mask, top_offset)

        return is_bottom_overlapping or is_top_overlapping

    def move(self):
        """
        Since the bird stays in a locked position, we move
        the pipes to the left to simulate the bird moving
        """
        self.pos_x -= self.VELOCITY

    def draw(self, window: pygame.Surface):
        window.blit(self.bottom_img, (self.pos_x, self.bottom_y))
        window.blit(self.top_img, (self.pos_x, self.top_y))

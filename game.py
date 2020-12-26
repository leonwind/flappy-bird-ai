import pygame
import os
from bird import Bird
from pipe import Pipe

class Game:

    IMG_PATH = "images/"
    WIDTH = 600
    HEIGHT = 800 

    def __init__(self):

        pipe_img: pygame.Surface = pygame.transform.scale2x(
            pygame.image.load(os.path.join(self.IMG_PATH, "pipe.png")).convert_alpha())
        background_img: pygame.Surface = pygame.transform.scale(
            pygame.image.load(os.path.join(self.IMG_PATH, "background.png")).convert_alpha(), 
            (self.WIDTH, self.HEIGHT))


if __name__ == "__main__":
    pass
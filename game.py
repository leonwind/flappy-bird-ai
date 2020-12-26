import pygame
import os
from ground import Ground
from bird import Bird
from pipe import Pipe

class Game:

    IMG_PATH = "images/"
    WIDTH = 500
    HEIGHT = 1000
    NUM_FPS = 30
    GROUND_HEIGHT = 750
    BIRD_X_POS = 200
    BIRD_Y_POS = 200

    def __init__(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.background_img: pygame.Surface = pygame.transform.scale(
            pygame.image.load(os.path.join(self.IMG_PATH, "background.png")).convert_alpha(), 
            (self.WIDTH, self.HEIGHT))
        self.ground_img: pygame.Surface = pygame.transform.scale2x(
            pygame.image.load(os.path.join(self.IMG_PATH, "ground.png")).convert_alpha())
        self.pipe_img: pygame.Surface = pygame.transform.scale2x(
            pygame.image.load(os.path.join(self.IMG_PATH, "pipe.png")).convert_alpha())
        self.bird_img: pygame.Surface = pygame.transform.scale2x(
            pygame.image.load(os.path.join(self.IMG_PATH, "bird1.png")).convert_alpha())

        self.ground = Ground(850, self.ground_img)

        self.bird = Bird(self.BIRD_X_POS, self.BIRD_Y_POS, self.bird_img)
        self.bird.draw(self.window)


    def update_window(self, pipes: list[Pipe]):
        self.window.blit(self.background_img, (0, 0))
        self.ground.draw(self.window)
        self.bird.draw(self.window)

        for pipe in pipes:
            pipe.draw(self.window)

        pygame.display.update()

    def run_game(self):
        clock = pygame.time.Clock()

        pipes = [Pipe(700, self.pipe_img)]

        run = True
        i = 0
        while run:
            clock.tick(self.NUM_FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            for pipe in pipes:
                if pipe.is_colliding(self.bird):
                    print("IS COLLIDING")
                    run = False
                pipe.move()

            self.bird.move() 
            self.update_window(pipes)

            if i % 10 == 0:
                self.bird.jump()
                pass
            i += 1
        

if __name__ == "__main__":
    game = Game()
    game.run_game()
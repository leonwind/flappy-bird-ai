import pygame
import os
from ground import Ground
from bird import Bird
from pipe import Pipe

class Game:

    IMG_PATH = "images/"
    WIDTH = 650
    HEIGHT = 1000
    NUM_FPS = 30
    GROUND_HEIGHT = 850
    BIRD_X_POS = 150
    BIRD_Y_POS = 400 
    PIPE_START_X = 700
    SPACE_BETWEEN_PIPES = WIDTH / 2

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

        self.ground = Ground(self.GROUND_HEIGHT, self.ground_img)

        self.bird = Bird(self.BIRD_X_POS, self.BIRD_Y_POS, self.bird_img)
        self.bird.draw(self.window)


    def update_window(self, pipes: list[Pipe]):
        self.window.blit(self.background_img, (0, 0))
        self.bird.draw(self.window)

        for pipe in pipes:
            pipe.draw(self.window)

        self.ground.draw(self.window)
        pygame.display.update()

    def run_game(self):
        clock = pygame.time.Clock()

        pipes = [Pipe(self.PIPE_START_X, self.pipe_img)]

        to_remove = set()

        run = True
        i = 0
        while run:
            clock.tick(self.NUM_FPS)

            if (self.ground.is_colliding(self.bird)):
                print("IS COLLIDING WITH FLOOR")
                #run = False

            for index, pipe in enumerate(pipes):
                if pipe.is_colliding(self.bird):
                    print("IS COLLIDING")
                    #run = False

                if pipe.pos_x <= self.PIPE_START_X - self.SPACE_BETWEEN_PIPES and len(pipes) <= 1:
                    pipes.append(Pipe(self.PIPE_START_X, self.pipe_img))

                if pipe.pos_x <= -self.pipe_img.get_width():

                    to_remove.add(index) 

                pipe.move()

            for index in to_remove:
                pipes.pop(index)
            to_remove.clear()

            #self.bird.move() 
            self.update_window(pipes)

            if i % 10 == 0:
                #self.bird.jump()
                pass
            i += 1

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()
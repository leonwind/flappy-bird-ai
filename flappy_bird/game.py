import os
import pygame
import argparse
from flappy_bird.ground import Ground
from flappy_bird.bird import Bird
from flappy_bird.pipe import Pipe


class Game:
    IMG_PATH = "images/"
    WIDTH = 650
    HEIGHT = 1000
    GROUND_HEIGHT = 850
    PIPE_START_X = 700
    SPACE_BETWEEN_PIPES = 400
    BIRD_X_POS = 150
    BIRD_Y_POS = 400
    NUM_FPS = 30

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
            pygame.image.load(os.path.join(self.IMG_PATH, "bird2.png")).convert_alpha())

        self.ground = Ground(self.GROUND_HEIGHT, self.ground_img)
        self.bird = Bird(self.BIRD_X_POS, self.BIRD_Y_POS, self.bird_img)

    def update_window(self, pipes: list[Pipe]):
        """Update the position of the bird and the pipes in the game window"""
        self.window.blit(self.background_img, (0, 0))
        self.bird.draw(self.window)

        for pipe in pipes:
            pipe.draw(self.window)

        self.ground.draw(self.window)
        pygame.display.update()

    def create_population(self):
        pass

    def play_game(self) -> int:
        """Run the game and return the score"""
        clock = pygame.time.Clock()

        pipes = [Pipe(self.PIPE_START_X, self.pipe_img)]
        to_remove = set()

        score = 0
        run = True
        while run:
            clock.tick(self.NUM_FPS)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.bird.jump()

            if self.ground.is_colliding(self.bird):
                run = False

            for index, pipe in enumerate(pipes):
                pipe.move()

                if pipe.passed:
                    if pipe.pos_x + self.pipe_img.get_width() <= 0:
                        to_remove.add(index)
                    continue

                if pipe.is_colliding(self.bird):
                    run = False

                if pipe.pos_x <= self.PIPE_START_X - self.SPACE_BETWEEN_PIPES and len(pipes) < 2:
                    pipes.append(Pipe(self.PIPE_START_X, self.pipe_img))

                if pipe.pos_x + self.pipe_img.get_width() <= self.BIRD_X_POS:
                    pipe.passed = True
                    score += 1

            for index in to_remove:
                pipes.pop(index)
            to_remove.clear()

            self.bird.move()
            self.update_window(pipes)

        pygame.quit()
        return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the game flappy bird")
    parser.add_argument("-play", action="store_true")
    args = parser.parse_args()

    game = Game()
    if args.play or True:
        # Let the player play flappy bird
        print("Score: {}".format(game.play_game()))
    else:
        # Let the AI play flappy bird
        game.create_population()

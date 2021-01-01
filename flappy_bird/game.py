import os
from typing import List, Tuple
import pygame
import argparse

from flappy_bird.ground import Ground
from flappy_bird.bird import Bird
from flappy_bird.pipe import Pipe
from neat.config import Config
from neat.population import Population
from neat.genotype.genome import Genome
from neat.neural_nets.feed_forward_net import FeedForwardNet


class Game:
    IMG_PATH = "flappy_bird/images/"
    WIDTH = 650
    HEIGHT = 1000
    GROUND_HEIGHT = 850
    PIPE_START_X = 700
    SPACE_BETWEEN_PIPES = 400
    BIRD_START_X = 150
    BIRD_START_Y = 400
    NUM_FPS = 30
    TANH_THRESHOLD = 0.5
    POPULATION_SIZE = 1

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

    def update_window(self, pipes: List[Pipe], birds: List[Bird]):
        """Update the position of the bird and the pipes in the game window"""
        self.window.blit(self.background_img, (0, 0))

        for bird in birds:
            if bird.alive:
                bird.draw(self.window)

        for pipe in pipes:
            pipe.draw(self.window)

        self.ground.draw(self.window)
        pygame.display.update()

    def evaluate_pipes(self, pipes: List[Pipe], bird: Bird) -> Tuple[Pipe, bool, bool]:
        """
        Check for a current bird if he collides with any pipe or passes one
        Also return the nearest pipe in front of the pipe
        """
        to_remove = set()
        is_colliding = False
        passed_pipe = False

        for index, pipe in enumerate(pipes):
            pipe.move()

            if pipe.passed:
                if pipe.pos_x + self.pipe_img.get_width() <= 0:
                    to_remove.add(index)
                continue

            if pipe.is_colliding(bird):
                is_colliding = True

            if pipe.pos_x <= self.PIPE_START_X - self.SPACE_BETWEEN_PIPES and len(pipes) < 2:
                pipes.append(Pipe(self.PIPE_START_X, self.pipe_img))

            if pipe.pos_x <= self.BIRD_START_X:
                pipe.passed = True
                passed_pipe = True

        for index in to_remove:
            pipes.pop(index)
        to_remove.clear()

        front_pipe = pipes[0] if not pipes[0].passed else pipes[1]
        return front_pipe, passed_pipe, is_colliding

    def create_population(self):
        """Create a population for the neat algorithm"""
        config: Config = Config(
            connection_mutation_rate=0.8,
            change_weight_mutation_rate=0.9,
            add_node_mutation_rate=0.05,
            add_connection_mutation_rate=0.5,
            reenable_connection_rate=0.25,
            species_elitism=2,
            max_stagnation=20,
            population_size=self.POPULATION_SIZE,
            num_input_neurons=3,
            num_output_neurons=1,
            num_of_generations=100,
            species_difference=3,
            genomes_to_save=0.8,
            activation_function="tanh"
        )

        population: Population = Population(config)
        population.run(self.evaluate_genomes)

    def evaluate_genomes(self, genomes: List[Genome], config: Config):
        """
        Play the game based on the output of the neural net for each genome / bird to
        evaluate the genomes
        """
        num_populations = len(genomes)
        clock = pygame.time.Clock()

        pipes = [Pipe(self.PIPE_START_X, self.pipe_img)]

        neural_nets: List[FeedForwardNet] = []
        birds: List[Bird] = []
        score = []
        for genome in genomes:
            neural_nets.append(FeedForwardNet.create(genome, config))
            birds.append(Bird(self.BIRD_START_X, self.BIRD_START_Y, self.bird_img))
            score.append(0)

        num_alive = num_populations

        run = True
        while run:
            clock.tick(3)

            for i in range(num_populations):
                print("{} are left alive".format(num_alive))
                curr_bird = birds[i]

                if not curr_bird.alive:
                    continue

                next_pipe, passed_pipe, is_colliding = self.evaluate_pipes(pipes, curr_bird)

                if is_colliding or self.ground.is_colliding(curr_bird):
                    curr_bird.alive = False
                    genomes[i].fitness -= 1
                    print("BIRD DIED")
                    num_alive -= 1
                    continue

                if passed_pipe:
                    score[i] += 1
                    genomes[i].fitness += 1

                # use the height of the bird and the distance to the top and bottom
                # pipe as the input weights
                input_weights = [curr_bird.pos_y,
                                 curr_bird.pos_y - next_pipe.top_y,
                                 curr_bird.pos_y - next_pipe.bottom_y]

                outputs = neural_nets[i].activate(input_weights)
                if outputs[0] > self.TANH_THRESHOLD:
                    curr_bird.jump()

                # give extra 0.1 fitness for each frame the bird survives
                genomes[i].fitness += 0.1

                curr_bird.move()

            if num_alive == 0:
                run = False

            self.update_window(pipes, birds)
        print(score)

    def play_game(self) -> int:
        """Let the user play the game"""
        clock = pygame.time.Clock()

        bird = Bird(self.BIRD_START_X, self.BIRD_START_Y, self.bird_img)
        pipes = [Pipe(self.PIPE_START_X, self.pipe_img)]

        score = 0
        run = True
        while run:
            clock.tick(self.NUM_FPS)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

            if self.ground.is_colliding(bird):
                run = False

            _, passed_pipe, is_colliding = self.evaluate_pipes(pipes, bird)

            if is_colliding:
                run = False

            if passed_pipe:
                score += 1

            bird.move()
            self.update_window(pipes, [bird])

        pygame.quit()
        return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the game flappy bird")
    parser.add_argument("-play", action="store_true")
    args = parser.parse_args()

    game = Game()
    if args.play:
        # Let the player play flappy bird
        print("Score: {}".format(game.play_game()))
    else:
        # Let the AI play flappy bird
        game.create_population()

from typing import List
import numpy as np
import random

from neat.config import Config
from neat.genotype.genome import Genome
from neat.specie import Specie
from neat.crossover import Crossover
from neat.mutation import Mutation


class Population:

    def __init__(self, config: Config):
        self.config = config
        self.population: List[Genome] = self._create_new_population()
        self.species: List[Specie] = []
        self.best_genome = None
        self.best_fitness = float("-inf")

        for genome in self.population:
            self._assign_specie(genome, 0)

    def _create_new_population(self) -> List[Genome]:
        population: List[Genome] = []

        for i in range(self.config.population_size):
            genome = Genome()
            inputs = []
            outputs = []

            for j in range(self.config.num_input_neurons):
                inputs.append(genome.create_new_node("input"))

            for j in range(self.config.num_output_neurons):
                outputs.append(genome.create_new_node("output"))

            for input_node in inputs:
                for output_node in outputs:
                    genome.create_new_edge(input_node.id, output_node.id)

            population.append(genome)
        return population

    def _assign_specie(self, genome: Genome, generation):
        """
        Assign a genome its proper specie
        :param genome: Genome to be assigned a specie
        :param generation: Current generation
        :return:
        """
        for specie in self.species:
            if Specie.species_distance(specie.genome, genome) < self.config.species_difference:
                genome.specie = specie.specie_id
                specie.members.append(genome)
                return

        # if no existing specie is equal enough, create a new one
        new_species = Specie(len(self.species), genome, generation)
        new_species.members.append(genome)
        genome.specie = new_species.specie_id
        self.species.append(new_species)

    def run(self, evaluation_function):
        for curr_gen in range(self.config.num_of_generations):
            # run flappy bird and change the fitness of each genome depending how good
            # the bird of the genome plays
            evaluation_function(self.population)

            for genome in self.population:
                if genome.fitness > self.best_fitness:
                    self.best_genome = genome
                    self.best_fitness = genome.fitness

            min_fitness = float("inf")
            max_fitness = float("-inf")

            for specie, is_stagnant in Specie.stagnation(self.species, curr_gen, self.config):
                if is_stagnant:
                    self.species.remove(specie)
                else:
                    for genome in specie.members:
                        min_fitness = min(min_fitness, genome.fitness)
                        max_fitness = max(max_fitness, genome.fitness)

            sum_adjusted_fitness = 0

            # should be at least one for adjusted fitness formula
            diff_fitness = max(1, max_fitness - min_fitness)
            for specie in self.species:
                avg_specie_fitness = np.mean([genome.fitness for genome in specie.members])
                adjusted_fitness = (avg_specie_fitness - min_fitness) / diff_fitness
                specie.adjusted_fitness = adjusted_fitness
                sum_adjusted_fitness += adjusted_fitness

            new_population: List[Genome] = []
            for specie in self.species:
                if specie.adjusted_fitness > 0:
                    size = max(2, int((specie.adjusted_fitness / sum_adjusted_fitness) *
                                      self.config.population_size))
                else:
                    size = 2

                survivors = specie.members
                survivors.sort(key=lambda g: g.fitness, reverse=True)
                specie.members = []

                purge_index = max(2, round(self.config.genomes_to_save * len(survivors)))
                survivors = survivors[:purge_index]

                # TODO: Always add the best genome in specie?
                for i in range(size):
                    parent_a: Genome = random.choice(survivors)
                    parent_b: Genome = random.choice(survivors)

                    child: Genome = Crossover.crossover(parent_a, parent_b, self.config)
                    Mutation.mutate(child, self.config)
                    new_population.append(child)

            for genome in new_population:
                self._assign_specie(genome, curr_gen)

            self.population = new_population

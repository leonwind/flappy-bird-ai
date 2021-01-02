from __future__ import annotations
from typing import List, Tuple
import numpy as np
import random

from neat.config import Config
from neat.genotype.genome import Genome
import neat.genotype.distance as distance
from neat.specie import Specie
import neat.crossover as crossover
import neat.mutation as mutation
import neat.stagnation as stagnation


class Population:

    def __init__(self, population: List[Genome], species: List[Specie], config: Config):
        self.population: List[Genome] = population
        self.species: List[Specie] = species
        self.config: Config = config

    def run(self, evaluation_function):
        for curr_gen in range(self.config.num_of_generations):
            print("GENERATION: {}".format(curr_gen))
            # run flappy bird and change the fitness of each genome depending how good
            # the bird of the genome plays
            evaluation_function(self.population, self.config)
            # Generate a new population by reproducing the non stagnated species
            self.population, self.species = self._reproduce(self.species, curr_gen, self.config)

    @staticmethod
    def _reproduce(species: List[Specie], curr_gen, config: Config) -> Tuple[List[Genome], List[Specie]]:
        """
        Filter out stagnated species and crossover the remaining species
        # Source: https://github.com/CodeReclaimers/neat-python/blob/master/neat/reproduction.py#L84
        """
        min_fitness = float("inf")
        max_fitness = float("-inf")
        print(species)
        for specie in species:
            print("CURR NUM MEMBERS: " + str(len(specie.members)))
        remaining_species = []

        for specie, is_stagnant in stagnation.stagnation(species, curr_gen, config):
            if not is_stagnant:
                remaining_species.append(specie)
                for genome in specie.members:
                    min_fitness = min(min_fitness, genome.fitness)
                    max_fitness = max(max_fitness, genome.fitness)

        print(max_fitness, min_fitness)

        if not remaining_species:
            return [], []

        # should be at least one for adjusted fitness formula
        diff_fitness = max(1, max_fitness - min_fitness)
        sum_adjusted_fitness = 0
        for specie in remaining_species:
            avg_specie_fitness = np.mean(specie.get_all_fitnesses())
            adjusted_fitness = (avg_specie_fitness - min_fitness) / diff_fitness

            specie.adjusted_fitness = adjusted_fitness
            sum_adjusted_fitness += adjusted_fitness

        new_population: List[Genome] = []
        for specie in remaining_species:
            if specie.adjusted_fitness > 0:
                size = max(2, int((specie.adjusted_fitness / sum_adjusted_fitness) * config.population_size))
            else:
                size = 2

            survivors = specie.members
            survivors.sort(key=lambda g: g.fitness, reverse=True)
            # kill all old members
            specie.members = []

            new_population.append(survivors[0])
            size -= 1

            # keep at least 2 genomes
            purge_index = max(2, int(config.genomes_to_save * len(survivors)))
            survivors = survivors[:purge_index]

            for i in range(size):
                parent_a: Genome = random.choice(survivors)
                parent_b: Genome = random.choice(survivors)

                child: Genome = crossover.crossover(parent_a, parent_b, config)
                mutation.mutate(child, config)
                new_population.append(child)

        for genome in new_population:
            remaining_species = Population._assign_specie([genome], remaining_species, curr_gen, config)

        return new_population, remaining_species

    @staticmethod
    def _assign_specie(genomes: List[Genome], species: List[Specie], curr_gen, config: Config) -> List[Specie]:
        """
        Assign a genome its proper specie
        :param genomes: Genomes to be assigned a specie
        :param species: Currently existing species, can be empty
        :param curr_gen: Current generation
        :return:
        """
        for genome in genomes:
            found_existing_specie = False

            for specie in species:
                compatibility = distance.calculate_compatibility_score(specie.representative, genome)
                print(compatibility, config.species_difference)
                if compatibility < config.species_difference:
                    genome.specie = specie.specie_id
                    specie.members.append(genome)
                    found_existing_specie = True
                    break

            if found_existing_specie:
                continue

            print("CREATE NEW SPECIE")
            # if no existing specie is similar enough, create a new one
            new_species = Specie(len(species), curr_gen)
            new_species.representative = genome
            new_species.members.append(genome)
            genome.specie = new_species.specie_id
            species.append(new_species)

        return species

    @staticmethod
    def create(config: Config) -> Population:
        population: List[Genome] = []

        for i in range(config.population_size):
            genome = Genome()
            inputs = []
            outputs = []

            for j in range(config.num_input_neurons):
                inputs.append(genome.create_new_node("input"))

            for j in range(config.num_output_neurons):
                outputs.append(genome.create_new_node("output"))

            for input_node in inputs:
                for output_node in outputs:
                    genome.create_new_edge(input_node.id, output_node.id)

            population.append(genome)

        species: List[Specie] = []
        Population._assign_specie(population, species, 0, config)

        return Population(population, species, config)

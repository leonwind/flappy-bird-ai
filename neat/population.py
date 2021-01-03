from __future__ import annotations
from typing import List, Dict
import numpy as np
import random
import math
from itertools import count

from neat.config import Config
from neat.genotype.genome import Genome
from neat.specie import Specie, SpeciesContainer
from neat.crossover import crossover
from neat.mutation import mutate
import neat.stagnation as stagnation


class Population:

    def __init__(self, population: Dict[int, Genome], genome_indexer, config: Config):
        self.population: Dict[int, Genome] = population
        self.species: SpeciesContainer = SpeciesContainer(config)
        # genome_indexer is a count object
        # could not find any type hint for an iterator
        self.genome_indexer = genome_indexer
        self.config: Config = config

        # assign each genome a specie
        self.species.assign_specie(self.population, 0)

    def run(self, evaluation_function):
        for curr_gen in range(self.config.num_of_generations):
            print("GENERATION: {}".format(curr_gen))
            # run flappy bird and change the fitness of each genome depending how good
            # the bird of the genome plays
            evaluation_function(list(self.population.values()), self.config)

            # Generate a new population by reproducing the non stagnated species
            self.reproduce(curr_gen)

            # Assign each genome in the new population a new specie again
            self.species.assign_specie(self.population, curr_gen)

    def reproduce(self, curr_gen):
        """
        Filter out stagnated species and crossover the remaining species
        # Source: https://github.com/CodeReclaimers/neat-python/blob/master/neat/reproduction.py#L84
        """
        min_fitness = float("inf")
        max_fitness = float("-inf")
        remaining_species = []

        for specie_id, specie, is_stagnant in stagnation.stagnation(self.species, curr_gen, self.config):
            if not is_stagnant:
                remaining_species.append(specie)
                for genome in specie.members:
                    min_fitness = min(min_fitness, genome.fitness)
                    max_fitness = max(max_fitness, genome.fitness)

        if not remaining_species:
            return

        # should be at least one for adjusted fitness formula
        diff_fitness = max(1, max_fitness - min_fitness)
        for specie in remaining_species:
            avg_specie_fitness = np.mean(specie.get_all_fitnesses())
            specie.adjusted_fitness = (avg_specie_fitness - min_fitness) / diff_fitness

        adjusted_fitnesses = [specie.adjusted_fitness for specie in remaining_species]
        previous_sizes = [len(specie.members) for specie in remaining_species]
        number_offsprings = Population._compute_new_specie_size(
            adjusted_fitnesses, previous_sizes, self.config.population_size, self.config.min_specie_size)

        new_population: Dict[int, genome] = {}
        for specie, size in zip(remaining_species, number_offsprings):
            survivors = specie.members
            survivors.sort(key=lambda g: g.fitness, reverse=True)
            # kill all old members
            specie.members = []

            for i in range(self.config.species_elitism):
                if size > 0:
                    key = next(self.genome_indexer)
                    new_population[key] = survivors[i]
                    size -= 1

            if size <= 0:
                continue

            purge_index = max(2, math.ceil(self.config.genomes_to_save * len(survivors)))
            survivors = survivors[:purge_index]

            for i in range(size):
                parent_a: Genome = random.choice(survivors)
                parent_b: Genome = random.choice(survivors)

                child: Genome = crossover(parent_a, parent_b, self.config)
                mutate(child, self.config)
                key = next(self.genome_indexer)
                new_population[key] = child

        self.population = new_population

    @staticmethod
    def _compute_new_specie_size(adjusted_fitnesses, previous_sizes, population_size, min_species_size) -> List[int]:
        """Compute the proper number of offspring per species (proportional to fitness)."""
        adjusted_fitness_sum = sum(adjusted_fitnesses)

        num_offsprings = []
        for adjusted_fitness, prev_size in zip(adjusted_fitnesses, previous_sizes):
            if adjusted_fitness > 0:
                size = max(min_species_size, (adjusted_fitness / adjusted_fitness_sum) * population_size)
            else:
                size = min_species_size

            avg = (size - prev_size) / 2
            num_spawns = prev_size
            if round(avg) != 0:
                num_spawns += avg
            elif avg > 0:
                num_spawns += 1
            else:
                num_spawns -= 1
            num_offsprings.append(num_spawns)

        total_offsprings = sum(num_offsprings)
        normalize_factor = population_size / total_offsprings
        return [max(min_species_size, round(num_spawns * normalize_factor)) for num_spawns in num_offsprings]

    @staticmethod
    def create(config: Config) -> Population:
        genome_indexer = count(1)
        population: Dict[int, Genome] = {}

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

            key = next(genome_indexer)
            population[key] = genome

        return Population(population, genome_indexer, config)

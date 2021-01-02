from typing import List
import numpy as np
from neat.specie import Specie
from neat.config import Config


def stagnation(species: List[Specie], generation, config: Config):
    """
    Keeps track of whether species are making progress
    and helps remove ones that are not.
    Look for the species which have not improved in max_stagnation generations
    Source: https://github.com/CodeReclaimers/neat-python/blob/master/neat/stagnation.py
    """
    species_data = []
    for specie in species:

        if not len(specie.members):
            continue

        if len(specie.fitness_history):
            max_fitness = max(specie.fitness_history)
        else:
            max_fitness = float("-inf")

        # TODO: Try out max for the specie fitness
        specie.fitness = int(np.mean(specie.get_all_fitnesses()))
        specie.fitness_history.append(specie.fitness)
        specie.adjusted_fitness = None

        if max_fitness < specie.fitness:
            specie.last_improved = generation

        species_data.append(specie)

    species_data.sort(key=lambda s: s.fitness)

    result = []
    num_non_stagnant = len(species_data)
    for index, specie in enumerate(species_data):
        # Override stagnant state if marking this species as stagnant would
        # result in the total number of species dropping below the limit.
        # Because species are in ascending fitness order, less fit species
        # will be marked as stagnant first.
        stagnant_time = generation - specie.last_improved

        is_stagnant = False

        if num_non_stagnant > config.species_elitism:
            is_stagnant = (stagnant_time > config.max_stagnation)

        if len(species_data) - index <= config.species_elitism:
            is_stagnant = False

        if is_stagnant:
            num_non_stagnant -= 1

        result.append((specie, is_stagnant))
    return result

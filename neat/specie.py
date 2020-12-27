from typing import List, Optional
from neat.genotype.genome import Genome
from neat.config import Config


class Specie:

    def __init__(self, specie_id, genome: Genome, generation):
        self.specie_id = specie_id
        self.genome: Genome = genome
        self.members: List[Genome] = []
        self.generation = generation
        self.fitness: Optional[int] = None
        self.fitness_history: List[int] = []
        self.adjusted_fitness: Optional[int] = None
        self.last_improved = generation

    @staticmethod
    def species_distance(genome_a: Genome, genome_b: Genome) -> float:
        """
        We calculate the distance between genome_a and genome_b by
        the original formula described in the paper.
        Like the most implementations we do not diminish between
        the excess and the disjoint.
        Furthermore we also set the constants C1, C2, C3, and N equal to 1
        and thus do not need to use them in our calculation
        :param genome_a:
        :param genome_b:
        :return: distance between genome_a and genome_b
        """
        distance = genome_a.calculate_compatibility_distance(genome_b)
        avg_weight_diff = genome_a.calculate_avg_weight_difference(genome_b)

        return distance + avg_weight_diff

    @staticmethod
    def stagnation(species: List[Specie], generation, config: Config):
        """
        Keeps track of whether species are making progress
        and helps remove ones that are not.
        Look for the species which have not improved in max_stagnation generations
        source: https://github.com/CodeReclaimers/neat-python/blob/master/neat/stagnation.py
        """
        species_data = []
        for specie in species:
            if len(specie.fitness_history):
                max_fitness = max(specie.fitness_history)
            else:
                max_fitness = float("-inf")

            specie.fitness = max([g.fitness for g in specie.members])
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

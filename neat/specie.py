from __future__ import annotations
from typing import List, Optional, Dict
from itertools import count
from neat.genotype.genome import Genome
from neat.genotype.compatibility import calculate_compatibility_score


class Specie:

    def __init__(self, specie_id, generation):
        self.specie_id = specie_id
        self.representative: Optional[Genome] = None
        self.members: List[Genome] = []
        self.created = generation
        self.last_improved = generation
        self.fitness: Optional[int] = None
        self.adjusted_fitness: Optional[int] = None
        self.fitness_history: List[int] = []

    def get_all_fitnesses(self):
        return [genome.fitness for genome in self.members]

    def update(self, representative, members):
        self.representative = representative
        self.members = members


class SpeciesContainer:

    def __init__(self, config: Config):
        self.species: Dict[int, Specie] = {}
        self.specie_indexer = count(1)
        # a lookup from genome to specie based on the
        # genome_indexer and the specie_indexer as the ids
        self.config: Config = config

    def assign_specie(self, population: Dict[int, Genome], curr_gen):
        """Assign each genome in the population its proper specie"""
        unassigned = set(population)
        new_representatives: Dict[int, int] = {}
        new_members: Dict[int, List[Genome]] = {}

        # assign new representatives for each specie
        for specie_id, specie in self.species.items():
            best_candidate_score = float("inf")
            best_candidate_id = None
            for genome_id in unassigned:
                genome = population[genome_id]
                compatibility_score = calculate_compatibility_score(specie.representative, genome)
                if compatibility_score < best_candidate_score:
                    best_candidate_score = compatibility_score
                    best_candidate_id = genome_id

            new_representatives[specie_id] = best_candidate_id
            new_members[specie_id] = [population[best_candidate_id]]
            unassigned.remove(best_candidate_id)

        while unassigned:
            genome_id = unassigned.pop()
            genome = population[genome_id]

            best_candidate_score = float("inf")
            best_candidate_id = None

            for specie_id, representative_id in new_representatives.items():
                representative = population[representative_id]
                compatibility_score = calculate_compatibility_score(representative, genome)
                if compatibility_score < self.config.species_difference and compatibility_score < best_candidate_score:
                    best_candidate_score = compatibility_score
                    best_candidate_id = specie_id

            # found a specie to assign the genome to
            if best_candidate_id is not None:
                new_members[best_candidate_id].append(genome)
            # Have not found any species to which the genome can be assigned to
            # Create a new specie
            else:
                new_specie_id = next(self.specie_indexer)
                new_representatives[new_specie_id] = genome_id
                new_members[new_specie_id] = [genome]

        # Update class instance SpecieCollection
        for specie_id, representative_id in new_representatives.items():
            specie = self.species.get(specie_id)

            if specie is None:
                new_specie = Specie(specie_id, curr_gen)
                self.species[specie_id] = new_specie

            members = new_members[specie_id]
            self.species[specie_id].update(population[representative_id], members)

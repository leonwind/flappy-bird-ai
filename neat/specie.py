from __future__ import annotations
from typing import List, Optional
from neat.genotype.genome import Genome


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

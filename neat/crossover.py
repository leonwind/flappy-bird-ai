from copy import deepcopy
from typing import Optional

import neat.utils as utils
from neat.genotype.genome import Genome
from neat.genotype.genome_edge import GenomeEdge
from neat.genotype.genome_node import GenomeNode
from neat.config import Config


class Crossover:

    @staticmethod
    def crossover(parent_a: Genome, parent_b: Genome, config: Config) -> Genome:
        """
        Crossover two Genomes instances
        :param parent_a:
        :param parent_b:
        :param config:
        :return: Return the child of genome_a and genome_b
        """

        child = Genome()
        best_parent, other_parent = Crossover._order_parents(parent_a, parent_b)

        for edge in best_parent.edges:
            matching_edge: Optional[GenomeEdge] = \
                other_parent.get_edge_by_innovation_num(edge.innovation_num)

            if matching_edge is None or utils.rand_bool():
                child_edge = deepcopy(edge)
            else:
                child_edge = deepcopy(matching_edge)

            if not child_edge.is_enabled:
                if utils.rand_uni_val() < config.reenable_connection_rate \
                        or best_parent.get_edge_by_innovation_num(edge.innovation_num):
                    child_edge.is_enabled = True

            child.add_edge_copy(child_edge)

        for node in best_parent.nodes:
            matching_node: Optional[GenomeNode] = other_parent.get_node_by_id(node.id)

            if matching_node is None or utils.rand_bool():
                child_node = deepcopy(node)
            else:
                child_node = deepcopy(matching_node)

            child.add_node_copy(child_node)

        return child

    @staticmethod
    def _order_parents(genome_a: Genome, genome_b: Genome):
        """
        Order the parents of the new child in respect to the
        fitness
        :param genome_a:
        :param genome_b:
        :return: best parent, second best parent
        """

        if genome_a.fitness == genome_b.fitness:
            if len(genome_a.edges) == len(genome_b.edges):
                if utils.rand_bool():
                    return genome_a, genome_b
                return genome_b, genome_a

            if len(genome_a.edges) > len(genome_b.edges):
                return genome_a, genome_b
            return genome_b, genome_a

        if genome_a.fitness > genome_b.fitness:
            return genome_a, genome_b
        return genome_b, genome_a

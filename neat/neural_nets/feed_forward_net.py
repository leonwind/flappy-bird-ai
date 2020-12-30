from typing import List, Optional

from neat.neural_nets.activations import Activations
from neat.config import Config
from neat.genotype.genome import Genome
from neat.genotype.genome_edge import GenomeEdge


class FeedForwardNet:

    def __init__(self):
        pass

    @staticmethod
    def create(genome: Genome, config: Config):
        edges: List[GenomeEdge] = [edge for edge in genome.edges if edge.is_enabled]

        input_nodes = []
        output_nodes = []

        for node in genome.nodes:
            if node.node_type == "input":
                input_nodes.append(node)
            elif node.node_type == "output":
                output_nodes.append(node)

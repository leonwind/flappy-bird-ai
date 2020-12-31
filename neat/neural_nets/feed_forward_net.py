from __future__ import annotations
from typing import List, Optional

from neat.neural_nets.activations import Activations
from neat.neural_nets.activations import ActivationFunction
from neat.config import Config
from neat.genotype.genome import Genome
from neat.genotype.genome_node import GenomeNode
from neat.genotype.genome_edge import GenomeEdge


class FeedForwardNet:

    def __init__(
            self,
            input_neurons: List[GenomeNode],
            output_neurons: List[GenomeNode],
            activation_function: ActivationFunction,
            config: Config
    ):
        self.input_neurons: List[GenomeNode] = input_neurons
        self.output_neurons: List[GenomeNode] = output_neurons
        self.activation_function: ActivationFunction = activation_function
        self.config: Config = config

    def activate(self) -> float:
        """Activate the neural net and return its output"""
        pass

    @staticmethod
    def create(genome: Genome, config: Config) -> FeedForwardNet:
        """Generate a feed forward neural network from a given genome"""
        edges: List[GenomeEdge] = [edge for edge in genome.edges if edge.is_enabled]

        input_nodes = []
        output_nodes = []

        for node in genome.nodes:
            if node.node_type == "input":
                input_nodes.append(node)
            elif node.node_type == "output":
                output_nodes.append(node)

        activation_function = Activations.get(config.activation_function)
        return FeedForwardNet(input_nodes, output_nodes, activation_function, config)

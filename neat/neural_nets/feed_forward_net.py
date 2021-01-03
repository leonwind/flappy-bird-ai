from __future__ import annotations
from typing import List, Dict, Tuple, Set
from collections import deque

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
            output_ids: Set[int],
            bias: Dict[int, float],
            network_graph: Dict[int, List[Tuple[int, float]]],
            activation_function: ActivationFunction,
            config: Config
    ):
        self.input_neurons: List[GenomeNode] = input_neurons
        self.output_neurons: List[GenomeNode] = output_neurons
        self.output_ids: Set[int] = output_ids
        self.bias: Dict[int, float] = bias
        self.network_graph: Dict[int, List[Tuple[int, float]]] = network_graph
        self.activation_function: ActivationFunction = activation_function
        self.config: Config = config

    def activate(self, inputs) -> List[float]:
        """
        Activate the neural net and return the outputs for each output neuron
        :param inputs: The input values for the neural net provided by flappy bird
        :return List[float]: Values for all the output neurons applied with the activation function
        """
        if len(inputs) != len(self.input_neurons):
            raise RuntimeError(
                "Expected {0:n} inputs, got {1:n}".format(len(self.input_neurons), len(inputs)))

        node_weights = {}
        queue = deque()
        for node, value in zip(self.input_neurons, inputs):
            node_weights[node.id] = inputs[node.id]
            queue.append(node.id)

        while queue:
            front = queue.popleft()
            if front in self.output_ids:
                continue

            for neighbor, edge_weight in self.network_graph[front]:
                if neighbor in node_weights:
                    node_weights[neighbor] *= edge_weight
                    node_weights[neighbor] += self.bias[neighbor]
                else:
                    node_weights[neighbor] = node_weights[front] * edge_weight + self.bias[neighbor]

                node_weights[neighbor] = self.activation_function(node_weights[neighbor])
                queue.append(neighbor)

        return [node_weights[node.id] for node in self.output_neurons]

    @staticmethod
    def create(genome: Genome, config: Config) -> FeedForwardNet:
        """Receives a genome and returns its phenotype (Feed forward neural net)"""
        print(genome)

        input_nodes = []
        output_nodes = []
        bias = {}
        output_ids = set()

        for node in genome.nodes:
            if node.type == "input":
                input_nodes.append(node)
                bias[node.id] = node.bias
            elif node.type == "output":
                output_nodes.append(node)
                output_ids.add(node.id)
                bias[node.id] = 0
            else:
                bias[node.id] = node.bias

        edges: List[GenomeEdge] = [edge for edge in genome.edges if edge.is_enabled]
        network_graph: Dict[int, List[Tuple[int, float]]] = {}

        for edge in edges:
            if edge.from_id in network_graph:
                network_graph[edge.from_id].append((edge.to_id, edge.weight))
            else:
                network_graph[edge.from_id] = [(edge.to_id, edge.weight)]

        activation_function = Activations.get(config.activation_function)
        return FeedForwardNet(
            input_nodes,
            output_nodes,
            output_ids,
            bias,
            network_graph,
            activation_function,
            config
        )

    def __str__(self):
        return self.network_graph.__str__()

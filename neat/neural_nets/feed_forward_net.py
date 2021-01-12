from __future__ import annotations
from typing import List, Set

from neat.neural_nets.activations import Activations
from neat.neural_nets.activations import ActivationFunction
from neat.config import Config
from neat.genotype.genome import Genome
from neat.genotype.genome_edge import GenomeEdge


class FeedForwardNet:

    def __init__(
            self,
            input_neurons: List[int],
            output_neurons: List[int],
            neural_net,
            activation_function: ActivationFunction
    ):
        self.input_neurons = input_neurons
        self.output_neurons = output_neurons
        self.neural_net = neural_net
        self.activation_function: ActivationFunction = activation_function

    def activate(self, inputs) -> List[float]:
        """
        Activate the neural net and return the outputs for each output neuron
        :param inputs: The input values for the neural net provided by flappy bird
        :return List[float]: Values for all the output neurons applied with the activation function
        """
        if len(inputs) != len(self.input_neurons):
            raise RuntimeError(
                "Expected {0:n} inputs, got {1:n}".format(len(self.input_neurons), len(inputs)))

        values = {}
        for input_ids, value in zip(self.input_neurons, inputs):
            values[input_ids] = value

        for node_id, bias, links in self.neural_net:
            node_inputs = []

            for prev, weights in links:
                node_inputs.append(values[prev] * weights)

            values[node_id] = self.activation_function(bias + sum(node_inputs))

        return [values[i] for i in self.output_neurons]

    def __str__(self):
        return self.neural_net.__str__()

    @staticmethod
    def create(genome: Genome, config: Config) -> FeedForwardNet:
        """Create a feed forward net from a genome"""
        input_neurons = [node.id for node in genome.nodes if node.type == "input"]
        output_neurons = [node.id for node in genome.nodes if node.type == "output"]

        layers = FeedForwardNet.create_layers(input_neurons, output_neurons, genome.edges)
        neural_net = []
        for layer in layers:
            for node in layer:
                inputs = []
                for edge in genome.edges:
                    from_id, to_id = edge.from_id, edge.to_id

                    if to_id == node:
                        inputs.append((from_id, edge.weight))

                genome_node = genome.get_node_by_id(node)
                neural_net.append((node, genome_node.bias, inputs))

        return FeedForwardNet(input_neurons, output_neurons, neural_net, Activations.get(config.activation_function))

    @staticmethod
    def create_layers(inputs: List[int], outputs: List[int], edges: List[GenomeEdge]) -> List[Set[int]]:
        """Return all the layers of the feed forward network"""
        layers = []
        visited = set(inputs)

        required = FeedForwardNet.required_for_output(inputs, outputs, edges)

        while True:
            neighbors = set(edge.to_id for edge in edges if edge.from_id in visited and edge.to_id not in visited)

            next_layer = set()
            for node in neighbors:
                if node in required and all(edge.from_id in visited for edge in edges if edge.to_id == node):
                    next_layer.add(node)

            if not next_layer:
                break

            layers.append(next_layer)
            visited = visited.union(next_layer)
        return layers

    @staticmethod
    def required_for_output(inputs: List[int], outputs: List[int], edges: List[GenomeEdge]) -> Set[int]:
        """Return all nodes which are necessary for the output nodes"""
        required = set(outputs)
        visited = set(outputs)

        while True:
            prev_layer = set(edge.from_id for edge in edges if edge.to_id in visited and edge.from_id not in visited)

            if not prev_layer:
                break

            layer_nodes = set()
            for prev_id in prev_layer:
                for node in inputs:
                    if prev_id != node:
                        layer_nodes.add(prev_id)

            if not layer_nodes:
                break

            required = required.union(layer_nodes)
            visited = visited.union(prev_layer)

        return required

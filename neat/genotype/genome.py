from __future__ import annotations
import random
from typing import Optional, List

from neat.genotype.genome_edge import GenomeEdge
from neat.genotype.genome_node import GenomeNode


class Genome:

    def __init__(self):
        self.fitness = 0
        self.edges: List[GenomeEdge] = []
        self.nodes: List[GenomeNode] = []
        self.node_ids = set()
        self.innovation_nums = set()
        # the id of the Specie
        self.specie: Optional[int] = None

    def add_connection_mutation(self):
        """
        Add a single new connection gene with a random weight connecting
        two previously unconnected nodes
        """
        possible_inputs = [n for n in self.nodes if n.node_type != "output"]
        possible_outputs = [n for n in self.nodes if n.node_type != "input"]

        while possible_inputs and possible_outputs:
            input_node: GenomeNode = random.choice(possible_inputs)
            output_node: GenomeNode = random.choice(possible_outputs)

            new_edge = self.create_new_edge(input_node.id, output_node.id)
            if new_edge is not None:
                return
            possible_inputs.remove(input_node)
            possible_outputs.remove(output_node)

    def add_node_mutation(self):
        """
        Split an existing edge and insert a new node between the two
        previously connected nodes. Disable the old connection and give
        the connection into the new node a weight of 1 and the connection from
        the new node to the old one the old weight
        """
        edge_to_split: GenomeEdge = random.choice(self.edges)
        edge_to_split.is_enabled = False

        new_node: GenomeNode = self.create_new_node("hidden")

        self.create_new_edge(edge_to_split.from_id, new_node.id, weight=1)
        self.create_new_edge(new_node.id, edge_to_split.to_id, weight=edge_to_split.weight)

    def calculate_compatibility_distance(self, other_genome: Genome) -> int:
        """
        Calculate the compatibility score of this genome instance and
        other_genome. This implementation, like the most NEAT implementations,
        does not differ between the excess and the disjoint genes.
        """
        # TODO: Verify the score calculation
        distance = 0

        max_innovation_score = max(other_genome.innovation_nums, default=0)
        for edge in self.edges:
            if edge.innovation_num != max_innovation_score:
                distance += 1

        max_node_id = max([n.id for n in other_genome.nodes])
        for node in self.nodes:
            if node.id != max_node_id:
                distance += 1

        return distance

    def calculate_avg_weight_difference(self, other_genome: Genome) -> float:
        """
        Calculate the average weight difference between this genome instance and
        other_genome.
        :param other_genome:
        :return:
        """
        weight_diff = 0.0
        num_weights = 0

        for edge in self.edges:
            matching_edge: GenomeEdge = other_genome.get_edge_by_innovation_num(edge.innovation_num)
            if matching_edge is not None:
                weight_diff += float(edge.weight) - float(matching_edge.weight)
                num_weights += 1

        if num_weights == 0:
            return weight_diff
        return weight_diff / num_weights

    def get_node_by_id(self, node_id) -> Optional[GenomeNode]:
        """
        Return a genome node with the same id as node_id
        :param node_id: target id
        :return:
        """
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_edge_by_innovation_num(self, innovation_num) -> Optional[GenomeEdge]:
        """
        Return a genome edge with innovation_num as its innovation number
        :param innovation_num: target innovation number
        :return:
        """
        for edge in self.edges:
            if edge.innovation_num == innovation_num:
                return edge
        return None

    def add_node_copy(self, copy_node: GenomeNode):
        """

        :param copy_node:
        :return:
        """
        self.nodes.append(GenomeNode(copy_node.id, copy_node.node_type))

    def add_edge_copy(self, copy_edge: GenomeEdge):
        """
        :param copy_edge:
        :return:
        """
        new_edge = GenomeEdge(copy_edge.from_id, copy_edge.to_id, copy_edge.is_enabled)
        new_edge.set_weight(copy_edge.weight)
        new_edge.set_innovation_num(copy_edge.innovation_num)

        if self._is_valid_new_edge(new_edge.from_id, new_edge.to_id):
            self.edges.append(new_edge)
            self.node_ids.add(new_edge.from_id)
            self.node_ids.add(new_edge.to_id)
            self.innovation_nums.add(new_edge.innovation_num)
        else:
            print("NOT VALID")
            print(new_edge)

    def create_new_node(self, node_type) -> GenomeNode:
        new_node = GenomeNode(len(self.nodes), node_type)
        self.nodes.append(new_node)
        return new_node

    def create_new_edge(self, input_node_id, output_node_id, is_enabled=True, weight=None) -> Optional[GenomeEdge]:
        new_edge = GenomeEdge(input_node_id, output_node_id, is_enabled)

        if weight is not None:
            new_edge.set_weight(weight)

        if self._is_valid_new_edge(new_edge.from_id, new_edge.to_id):
            self.edges.append(new_edge)
            return new_edge
        return None

    def _is_valid_new_edge(self, from_id, to_id) -> bool:
        return not self._connection_exists(from_id, to_id) and \
               not self._creates_cycle(from_id, to_id)

    def _connection_exists(self, from_id, to_id) -> bool:
        """Check if a given edge already exists in the graph"""
        for edge in self.edges:
            if edge.from_id == from_id and edge.to_id == to_id:
                return True
        return False

    def _creates_cycle(self, from_id, to_id) -> bool:
        """Check if a given edge creates a cycle in the graph"""
        if from_id == to_id:
            return True

        visited = set()
        visited.add(from_id)

        while True:
            num_added = 0
            for edge in self.edges:
                if edge.to_id in visited and edge.from_id not in visited:
                    if edge.from_id == to_id:
                        return True
                    visited.add(edge.from_id)
                    num_added += 1

            if num_added == 0:
                return False

    def __str__(self):
        ret = "Nodes: "
        for node in self.nodes:
            ret += node.__str__() + " "

        ret += "\nEdges:\n"
        for edge in self.edges:
            ret += edge.__str__() + "\n"
        return ret

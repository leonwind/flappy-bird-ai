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
        self.species = None

    def add_connection_mutation(self):
        """
        Add a single new connection gene with a random weight connecting
        two previously unconnected nodes
        """
        possible_inputs = [n for n in self.nodes if n.node_type != "output"]
        possible_outputs = [n for n in self.nodes if n.node_type != "input"]

        if possible_inputs or possible_outputs:
            input_node: GenomeNode = random.choice(possible_inputs)
            output_node: GenomeNode = random.choice(possible_outputs)

            # TODO: check if connection is valid  
            new_edge = self._create_new_edge(input_node.id, output_node.id)
            self.edges.append(new_edge)

    def add_node_mutation(self):
        """
        Split an existing edge and insert a new node between the two
        previously connected nodes. Disable the old connection and give
        the connection into the new node a weight of 1 and the connection from
        the new node to the old one the old weight
        """
        edge_to_split: GenomeEdge = random.choice(self.edges)
        edge_to_split.is_enabled = False

        new_node: GenomeNode = self._create_new_node("hidden")

        self._create_new_edge(edge_to_split.from_id, new_node.id, weight=1)
        self._create_new_edge(new_node.id, edge_to_split.to_id, weight=edge_to_split.weight)

    def calculate_compatibility_distance(self, other_genome: Genome) -> int:
        """
        Calculate the compatibility score of this genome instance and
        other_genome. This implementation, like the most NEAT implementations,
        does not differ between the excess and the disjoint genes.
        """
        # TODO
        distance = 0

        max_innovation_score = max(other_genome.innovation_nums)
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
            matching_edge: GenomeEdge = other_genome.get_edge_by_innovtion_num(edge.innovation_num)
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
        self.nodes.append(copy_node)

    def add_edge_copy(self, copy_edge: GenomeEdge):
        """

        :param copy_edge:
        :return:
        """
        self.node_ids.add(copy_edge.from_id)
        self.node_ids.add(copy_edge.to_id)
        self.innovation_nums.add(copy_edge.innovation_num)
        self.edges.append(copy_edge)

    def _create_new_node(self, node_type) -> GenomeNode:
        new_node = GenomeNode(len(self.nodes), node_type)
        self.nodes.append(new_node)
        return new_node

    def _create_new_edge(self, input_node_id, output_node_id, is_enabled=True, weight=None) -> GenomeEdge:
        new_edge = GenomeEdge(input_node_id, output_node_id, is_enabled)

        if weight is not None:
            new_edge.set_weight(weight)

        self.edges.append(new_edge)
        return new_edge

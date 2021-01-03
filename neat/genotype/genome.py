from __future__ import annotations
import random
from typing import Optional, List

from neat.genotype.genome_edge import GenomeEdge
from neat.genotype.genome_node import GenomeNode


class Genome:

    def __init__(self):
        self.edges: List[GenomeEdge] = []
        self.nodes: List[GenomeNode] = []
        self.fitness = None
        # save the node ids and the innovation nums for faster lookup
        # while calculating the edge distance
        self.node_ids = set()
        self.innovation_nums = set()

    def mutate_add_edge(self):
        """Add a new edge between two unconnected nodes with a random weight"""
        possible_inputs = [node for node in self.nodes if node.type != "output"]
        possible_outputs = [node for node in self.nodes if node.type != "input"]

        if possible_inputs and possible_outputs:
            from_node: GenomeNode = random.choice(possible_inputs)
            to_node: GenomeNode = random.choice(possible_outputs)

            self.create_new_edge(from_node.id, to_node.id)

            # possible_inputs.remove(from_node)
            # possible_outputs.remove(to_node)

    def mutate_add_node(self):
        """
        Split up a existing edge into two edges and insert
        a new node in the middle.
        Disable the old edge and give the edge into the new node
        a weight of 1 and the edge from the new node the weight of
        the existing connection.
        """
        edge_to_split: GenomeEdge = random.choice(self.edges)
        edge_to_split.is_enabled = False

        new_node = self.create_new_node("hidden")
        self.create_new_edge(edge_to_split.from_id, new_node.id, weight=1)
        self.create_new_edge(new_node.id, edge_to_split.to_id, weight=edge_to_split.weight)

    def mutate_remove_node(self):
        """Remove a hidden node"""
        # TODO
        pass

    def mutate_remove_edge(self):
        """Remove an edge"""
        # TODO
        pass

    def create_new_node(self, node_type, next_id=None) -> GenomeNode:
        if next_id is None:
            next_id = len(self.nodes)
        new_node = GenomeNode(next_id, node_type)
        self.nodes.append(new_node)
        self.node_ids.add(next_id)
        return new_node

    def create_new_edge(self, from_id, to_id, is_enabled=True, weight=None) -> bool:
        """
        Create a new edge in the graph.
        Return True if the new edge is valid and could be added, otherwise return False.
        """
        new_edge = GenomeEdge(from_id, to_id, is_enabled)

        if weight is not None:
            new_edge.weight = weight

        if self._is_valid_new_edge(from_id, to_id):
            self.edges.append(new_edge)
            self.innovation_nums.add(new_edge.innovation_num)
            return True
        return False

    def get_node_by_id(self, target_id) -> Optional[GenomeNode]:
        for node in self.nodes:
            if node.id == target_id:
                return node
        return None

    def get_edge_by_innovation_num(self, innovation_num) -> Optional[GenomeEdge]:
        """Return the edge by its innovation number"""
        for edge in self.edges:
            if edge.innovation_num == innovation_num:
                return edge
        return None

    def _is_valid_new_edge(self, from_id, to_id) -> bool:
        """Check if a new edge is a valid edge for a feed forward neural net"""
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

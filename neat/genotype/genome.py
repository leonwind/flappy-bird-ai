import random
from genome_edge import GenomeEdge
from genome_node import GenomeNode

class Genome:

    def __init__(self):
        self.fitness = 0

        self.edges: list[GenomeEdge] = []
        self.nodes: list[GenomeNode] = []
        self.node_ids = set()
        self.innovation_nums = set()
        
        self.species = None

    
    def add_connection_mutation(self):
        """
        Add a single new connection gene with a random weight connecting
        two previously unconnected nodes
        """
        possible_inputs = [n for n in self.nodes if n.type != "output"]
        possible_outputs = [n for n in self.nodes if n.type != "input"]

        if possible_inputs or possible_outputs:
            input_node: GenomeNode = random.choice(possible_inputs)
            output_node: GenomeNode = random.choice(possible_outputs)

            # TODO: check if connection is valid  
            self._create_new_edge(input_node.id, output_node.id)

    def add_node_mutation(self):
        """
        Split an existing edge and insert a new node between the two
        previously connected nodes. Disable the old connection and give
        the connection into the new node a weight of 1 and the connection from
        the new node to the old one the old weight
        """
        edge_to_split: GenomeEdge = random.choice(self.edges)
        edge_to_split.is_enabled = False

        new_node: GenomeNode = _create_new_node(len(self.nodes), "hidden")
        self.nodes.append(new_node)

        edge_a = self._create_new_edge(edge_to_split.from_id, new_node.id, weight=1)
        edge_b = self._create_new_edge(new_node.id, edge_to_split.to_id, weight=edge_to_split.weight)

        self.edges.append(edge_a)
        self.edges.append(edge_b)

    def get_num_excess_genes(self, external_genome: Genome):
        """
        Genes which do not match are excess genes if the 
        innovation number of the nodes of this instance is greater than
        the maximum innovation number of external_genome
        """
        num_excess = 0

        max_innovation_num_external = max(external_genome.innovation_nums)

        for edge in self.edges:
            if edge.innovation_num > max_innovation_num_external:
                num_excess += 1

        return num_excess

    def get_num_disjoint_genes(self, external_genome: Genome):
        """
        Genes which do not match are disjoint genes if the 
        innovation number of the nodes of this instance is smaller than 
        the maximum innovation number of external_genome
        """
        num_disjoint = 0

        return num_disjoint

    def _create_new_node(self, node_type) -> GenomeNode:
        new_node = GenomeNode(len(self.nodes), node_type)
        self.nodes.append(new_node)
        return new_node

    def _create_new_edge(self, input_node_id, output_node_id, is_enabled=True, weight=None) -> GenomeEdge:
        new_edge = GenomeEdge(input_node_id, output_node_id, is_enabled)

        if weight is not None:
            new_edge.set_weight(weight)

        return new_edge        

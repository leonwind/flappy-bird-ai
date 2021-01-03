from neat.genotype.genome import Genome


def calculate_compatibility_score(genome_a: Genome, genome_b: Genome) -> float:
    """
    We calculate the genetic distance between genome_a and genome_b by
    the original formula described in the paper to find out if the genomes
    are compatible.
    Like the most implementations we do not diminish between
    the excess and the disjoint genes and set the constants C1, C2, and C3 to 1.
    """
    # TODO: Verify the calculation
    node_distance = _calculate_node_distance(genome_a, genome_b)
    edge_distance = _calculate_edge_distance(genome_a, genome_b)
    return node_distance + edge_distance


def _calculate_node_distance(genome_a: Genome, genome_b: Genome) -> float:
    node_distance = 0

    for node_a in genome_a.nodes:
        if node_a.id not in genome_b.node_ids:
            node_distance += 1

    for node_b in genome_b.nodes:
        if node_b.id not in genome_a.node_ids:
            node_distance += 1

    return node_distance / max(len(genome_a.nodes), len(genome_b.nodes))


def _calculate_edge_distance(genome_a: Genome, genome_b: Genome) -> float:
    edge_distance = 0

    for edge_a in genome_a.edges:
        if edge_a.innovation_num not in genome_b.innovation_nums:
            edge_distance += 1

    for edge_b in genome_b.edges:
        if edge_b.innovation_num not in genome_a.innovation_nums:
            edge_distance += 1

    return edge_distance / max(len(genome_a.edges), len(genome_b.edges))

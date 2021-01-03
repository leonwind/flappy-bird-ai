import neat.utils as utils
from neat.config import Config
from neat.genotype.genome import Genome


def mutate(genome: Genome, config: Config):
    """
    Apply mutation to genome at proper rate.
    Mutate either the connections by changing the weight or
    mutate the structure by adding new connections or split up connections
    :param genome: The genome to mutate
    :param config: The configuration with the mutation parameters
    """
    if utils.rand_uni_val() < config.add_node_mutation_rate:
        genome.mutate_add_node()

    if utils.rand_uni_val() < config.add_connection_mutation_rate:
        genome.mutate_add_edge()

    for node in genome.nodes:
        if utils.rand_uni_val() < config.change_weight_mutation:
            node.mutate()
        if utils.rand_uni_val() < config.replace_weight_mutation:
            node.generate_random_bias()

    for edge in genome.edges:
        if utils.rand_uni_val() < config.change_weight_mutation:
            edge.mutate()
        if utils.rand_uni_val() < config.replace_weight_mutation:
            edge.generate_random_weight()

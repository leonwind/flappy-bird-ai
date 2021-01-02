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
    if utils.rand_uni_val() < config.connection_mutation_rate:
        for edge in genome.edges:
            if utils.rand_uni_val() < config.change_weight_mutation_rate:
                difference = utils.rand_uni_val() * utils.pos_or_neg()
                edge.weight += difference
            else:
                edge.generate_random_weight()

    if utils.rand_uni_val() < config.add_node_mutation_rate:
        genome.mutate_add_node()

    if utils.rand_uni_val() < config.add_connection_mutation_rate:
        genome.mutate_add_edge()

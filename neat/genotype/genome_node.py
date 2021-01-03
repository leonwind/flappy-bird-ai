import numpy as np
import neat.utils as utils


class GenomeNode:

    def __init__(self, node_id, node_type):
        self.id: int = node_id
        # node_type is either input, hidden or output
        self.type: str = node_type
        self.bias = None
        self.generate_random_bias()

    def generate_random_bias(self):
        self.bias = np.random.normal(0, 1)

    def mutate(self):
        self.bias += utils.rand_uni_val() * utils.pos_or_neg()

    def __str__(self):
        return "{0}-{1}, bias: {2}".format(self.id, self.type, self.bias)

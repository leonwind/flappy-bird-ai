import numpy as np


class GenomeEdge:

    def __init__(self, from_id, to_id, is_enabled):
        self.from_id: int = from_id
        self.to_id: int = to_id
        self.is_enabled: bool = is_enabled
        self.weight = None
        self.generate_random_weight()
        # The innovation number is an unique int to identify an edge between two nodes
        # of different genomes
        self.innovation_num = self._calculate_innovation_num()

    def generate_random_weight(self):
        self.weight = np.random.normal(0, 1)

    def _calculate_innovation_num(self):
        """Generate unique innovation number for two nodes by using Cantors pairing function"""
        return 0.5 * (self.from_id + self.to_id) * (self.from_id + self.to_id + 1) + self.to_id

    def __str__(self):
        return "from: {} to: {} weight: {} enabled: {}" \
            .format(self.from_id, self.to_id, self.weight, self.is_enabled)

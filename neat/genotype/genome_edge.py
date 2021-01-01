import numpy as np


class GenomeEdge:

    def __init__(self, from_id, to_id, is_enabled):
        self.from_id: int = from_id
        self.to_id: int = to_id
        self.is_enabled: bool = is_enabled
        self.weight = None
        self.generate_random_weight()
        self.innovation_num = self._calculate_innovation_num()

    def generate_random_weight(self):
        self.weight = np.random.normal(0, 1)

    def set_weight(self, new_weight):
        self.weight = new_weight

    def _calculate_innovation_num(self):
        # TODO
        return 0

    def __str__(self):
        return "from: {}, to: {}, weight: {}, enabled: {}"\
            .format(self.from_id, self.to_id, self.weight, self.is_enabled)

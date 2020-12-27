import torch

class GenomeEdge:

    def __init__(self, from_id, to_id, is_enabled):
        self.from_id: int = from_id 
        self.to_id: int = to_id 
        self.is_enabled: bool = is_enabled

        self.weight = self.generate_weight_random()
        self.innovation_num = self._calculate_innovation_num()

    def generate_weight_random(self):
        return torch.Tensor(torch.normal(torch.arange(0, 1).float()))

    def set_weight(self, new_weight):
        self.weight = torch.Tensor([new_weight])

    def _calculate_innovation_num(self):
        # TODO
        pass
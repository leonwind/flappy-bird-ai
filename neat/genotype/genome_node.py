class GenomeNode:

    def __init__(self, node_id, node_type):
        self.id: int = node_id
        # node_type is either input, hidden or output
        self.type: str = node_type

    def __str__(self):
        return "{0}-{1}".format(self.id, self.type)

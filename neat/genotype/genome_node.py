class GenomeNode:

    def __init__(self, id, node_type):
        self.id: int = id 
        # node_type is either input, hidden or output
        self.node_type: str = node_type 

    def __str__(self):
        return "{0}-{1}".format(self.id, self.node_type)
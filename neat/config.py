class Config:

    def __init__(
            self,
            change_connection_mutation_rate,
            change_weight_mutation_rate,
            add_node_mutation_rate,
            add_connection_mutation_rate,
            reenable_connection_rate
    ):
        self.change_connection_mutation_rate = change_connection_mutation_rate
        self.change_weight_mutation_rate = change_weight_mutation_rate
        self.add_node_mutation_rate = add_node_mutation_rate
        self.add_connection_mutation_rate = add_connection_mutation_rate
        self.reenable_connection_rate = reenable_connection_rate

class Config:

    def __init__(
            self,
            change_weight_mutation,
            replace_weight_mutation,
            add_node_mutation_rate,
            add_connection_mutation_rate,
            reenable_connection_rate,
            species_elitism,
            max_stagnation,
            population_size,
            num_input_neurons,
            num_output_neurons,
            num_of_generations,
            species_difference,
            genomes_to_save,
            min_specie_size,
            activation_function
    ):
        """
        :param change_weight_mutation:
        The rate of which am edge weight or bias gets modified
        :param replace_weight_mutation:
        The rate of which an edge weight or bias gets new generated
        :param add_node_mutation_rate:
        The rate of which a new node gets inserted into an existing connection
        :param add_connection_mutation_rate:
        The rate of which a new connection gets inserted
        :param reenable_connection_rate:
        The rate of which a disabled connection gets re enabled again
        :param species_elitism:
        The number of species which survive
        :param max_stagnation:
        The maximum time which is a specie allowed to stagnate
        :param population_size:
        The population size
        :param num_input_neurons:
        Number of input neurons
        :param num_output_neurons:
        Number of output neurons
        :param num_of_generations:
        Number of generations to run
        :param species_difference:
        The maximum difference between two genomes to be put into the same specie
        :param genomes_to_save:
        The percentage of how many genomes per specie to save
        :param min_specie_size:
        The minimum numbers of genomes per specie
        :param activation_function:
        Which activation to use for the neural net
        """
        self.change_weight_mutation = change_weight_mutation
        self.replace_weight_mutation = replace_weight_mutation
        self.add_node_mutation_rate = add_node_mutation_rate
        self.add_connection_mutation_rate = add_connection_mutation_rate
        self.reenable_connection_rate = reenable_connection_rate
        self.species_elitism = species_elitism
        self.max_stagnation = max_stagnation
        self.population_size = population_size
        self.num_input_neurons = num_input_neurons
        self.num_output_neurons = num_output_neurons
        self.num_of_generations = num_of_generations
        self.species_difference = species_difference
        self.genomes_to_save = genomes_to_save
        self.min_specie_size = min_specie_size
        self.activation_function = activation_function

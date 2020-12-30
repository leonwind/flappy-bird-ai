class Config:

    def __init__(
            self,
            change_connection_mutation_rate,
            change_weight_mutation_rate,
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
            genomes_to_save
    ):
        """
        :param change_connection_mutation_rate:
        The rate of which each connection does get changed
        :param change_weight_mutation_rate:
        The rate of a connection to be changed just is slightly modifying its rate.
        If not, a new random weight gets chosen
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
        """
        self.change_connection_mutation_rate = change_connection_mutation_rate
        self.change_weight_mutation_rate = change_weight_mutation_rate
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

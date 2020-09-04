import individual
import utils
from random import Random
from collections.abc import Iterable

'''
TODO:

- DONE: change population_size attribute usage
    - create setter for attribute
    - change add_individual and add_individuals methods for  population_size attribute usage
        - prohibit adding individuals throuhg size restrictions (DON'T change size after adding individuals to the Population)

- DONE: Update size usages

- DONE: Restrict adding individuals to Population with different individual sizes
    - Set individual_size attribute for population Class (for intance or static?)

- DONE: URGENT: TEST ALL current functions


- DONE: set mutants (on empty individuals)
    - set mutants portion attribute (rename)

- DONE: make generation attribute as counter (rename) and set generation attribute for each Population instance

- DONE: CHECK rounding
--------------------------------------------------
- DONE: getElite and getNonElite (on elite_individuals atribute or list)
    - set elite portion attribute (rename)
    - set elite_individuals attibute

    Recieves: Nothing
    Returns: A List o elite individuals (OPTIONAL)*
    Overall desc: Sets the elite_individuals attribute for population (and returns it as well)*
    Execution:
        - Calculate the elite portion (multiply elite_portion*self.population_size)
        - Re-initialize elite_individuals in empty list (a Queue)
        - Compute and set highest 'n' quality valued individuals
        - return elite_individuals
        NOTE: the elite_individuals queue must pop the oldest pushed individual when its capacity is full
            and add it to the non_elite_individuals list

--------------------------------------------------

- DONE: sortIndividuals method by Individual fitness (sort the Individuals attribute)

--------------------------------------------------
- DONE: crossover (parameterized uniform crossover)
    - place the resulting offspring (Individual) into incomplete Population
        - Possible: consider the method as an Individual method
CROSSOVER
Recieves: two individuals as arguments and one as the treshold
Returns: New individual with 'paired' chromosome
-for each in individual_size (chromosome size)
    -generates a random number between 0 and 1
    -checks if the generated number is lower or greater than the treshold argument
    -assigns the correspondig chromosome field (vector value)
-return individual with generated chromosome
--------------------------------------------------

- DONE: calcualteAvgFittnes method
    - calculate and ...
    - set avg_elite_fitness attibute

- DONE: getFittestIndividual method
    - get the topmost Individual from elite_individuals (elite portion) or from sorted Individuals attribute
    - set fittest_individual attibute

- Check and implemented type checking were it's needed.

- Document functions properly.
    - Have into account to document with docstrings those fucntions which are meant to be used as API or interfaces to 
    the main program

NOTE:

Standard Typing:
- NOTE: Look into type, value and attribte checking for arguments passed to functions:
    development must be modular and reduced (meaning, small).
    Main checks:
        - check for number of arguments -> TypeError
        - check for type of arguments -> TypeError
        - check for value resticitions (domain and argument type) of arguments -> ValueError
        - check Underlying problem logic assigment to attributes -> AttributeError
        - EXTRA:  check how to enable arguemnt flexibility through parsing or other approach -> This would be a seperate module.
Duck Typing:
- NOTE: Only type check for the inputs which are usually obtained from the programs (user) interfaces:
    - If the program is an API, or a module to use as programming interface, type check for those parts of the program which the
    user is going to use.
    - IMPORTANT: Only type-check for the inputs recieved in interfaces to the program (inputs which may affect the exectuion of it
    or cause it to crask).
    - Don't type check for the parts that the developer/programmer is meant to know and way of usage. For the latter is best only
    to have well documented code; i.e. what goes in, what goes out, exceptions, overall code description, and overall work flow.
'''

#Population class (composed of many Individual instances)
class Population:
    generation = 0 #Counter
    population_size = 0
    individual_size = 0
    elite_portion = 0.0
    mutant_portion = 0.0

    #DONE
    #Initializer
    def __init__(self, *args: tuple):
        self.individuals = list()
        self.individual_size = 0
        self.population_size = 0
        self.elite_individuals = list()
        self.non_elite_individuals = list()
        Population.generation += 1
        self.generation = Population.generation
        #If size parameters 'args' are passed in...
        if len(args) > 2:
            raise TypeError("Population __init__() constructor expects 1 or 2 arguments, {} given.".format(len(args)))
        elif len(args) > 0:
            self.population_size = args[0]
            if len(args) == 2:
                self.individual_size = args[1]
        else:
            self.population_size = Population.population_size
            self.individual_size = Population.individual_size

    #DONE
    #Create Population of a specific (population_size) number of random Individual instances
    def create_random_population(self, *portion: tuple):
        amount = self.population_size
        #If the amount parameter 'arg' is passed in...
        if len(portion) > 1:
            raise TypeError("Population create_random_population() function expects 0 or 1 arguments, {} given.".format(len(portion)))
        elif len(portion) == 1:
            if not (isinstance(portion[0], float) or isinstance(portion[0], int)):
                raise TypeError("Passed 'portion' argument must be a numeric value ('float' or 'int'). Passed argument is of type: {}.".format(type(portion[0])))
            elif portion[0] > 1.0 or portion[0] < 0.0:
                raise ValueError("Passed 'portion' argument must be in between 0 and 1 [0.0, 1.0]. Passed argument is: {}.".format(portion[0]))
            amount = round(portion[0] * amount)
        #Populate the Population (individuals)
        if len(self.individuals) != 0: #Population had already been populated...
            self.individuals = list()
        for i in range(amount):
            self.individuals.append(individual.Individual(self.individual_size))

    #DONE
    #Gets and sets the elite individuals from the current population
    def get_elite(self):
        portion = round(self.population_size * Population.elite_portion)
        self.elite_individuals = utils.get_lowest_values(self.individuals, portion)
        return self.elite_individuals
    
    #DONE
    #Gets and sets the non-elite individuals from the current population
    def get_non_elite(self):
        if not self.individuals:
            portion = round(self.population_size * (1 - Population.elite_portion))
            self.non_elite_individuals = utils.get_highest_values(self.individuals, portion)
        else:
            for individual in self.individuals:
                if individual not in self.elite_individuals:
                    self.non_elite_individuals.append(individual)
        return self.non_elite_individuals
        #DIDNT WORK: self.non_elite_individuals = [individual for indiv in self.individuals if indiv not in self.elite_individuals]       
    
    #DONE
    #Classify the individuals population in elite and non-elite
    def classify_population(self):
        self.get_elite()
        self.get_non_elite()
    
    #DONE
    #Sort Population based on Individuals' quality attribute
    def sort_individuals(self):
        self.individuals.sort()
        return self.individuals

    #DONE
    #Creates an Individual offspring based on two distinct individuals randomly selected from different portions of a population (elite and non-elite)
    def crossover(self, treshold):
        random_instance = Random()
        elite_individual = random_instance.choice(self.elite_individuals)
        non_elite_individual = random_instance.choice(self.non_elite_individuals)
        new_chromosome = Population.parameterized_uniform_crossover(elite_individual.chromosome, non_elite_individual.chromosome, treshold)
        new_individual = individual.Individual(new_chromosome)
        return new_individual

    #DONE
    #Perform parameterized crossover among two list of the same size using a treshold for biasing
    @staticmethod
    def parameterized_uniform_crossover(first_list: list, second_list: list, treshold: int):
        if not (isinstance(first_list, Iterable)):
            raise TypeError("First provided argument, 'first_list', must be an iterable type. Provided argument is of type: {}.".format(type(first_list)))
        elif not isinstance(second_list, Iterable):
            raise TypeError("Second provided argument, 'second_list', must be an iterable type. Provided argument is of type: {}.".format(type(second_list)))
        elif not (isinstance(treshold, float) or isinstance(treshold, int)):
            raise TypeError("Third provided argument, 'treshold', must be numeric type ('float' or 'int'). Provided argument is of type: {}.".format(type(treshold)))
        elif treshold < 0 or treshold > 1:
            raise ValueError("Provided third argument, 'treshold', must be in between 0 an 1 [0.0, 1.0]. Value is: {}.".format(treshold))
        elif len(first_list) != len(second_list):
            raise ValueError("First two provided iterable arguments must both be of the same size. First argument is of size: {}. Second argument is of size: {}.".format(len(first_list), len(second_list)))
        random_instance = Random()
        result = list()
        for i in range(len(first_list)):
            random_value = random_instance.random()
            if random_value < treshold:
                result.append(first_list[i])
            else:
                result.append(second_list[i])
        return result

    #DONE
    #Calculate avg fitness or quality of a population instance
    def get_average_fitness(self):
        average = 0.0
        for individual in self.individuals:
            average += individual.quality
        return (average / self.population_size)
    
    #DONE
    #Calculate avg fitness or quality of a population's elite individuals
    def get_average_elite_fitness(self):
        average = 0.0
        for individual in self.elite_individuals:
            average += individual.quality
        return (average / len(self.elite_individuals))


    #DONE
    #Returns the fittest individual based on the Individual quality attribute
    def get_fittest_individual(self):
        fittest = utils.get_lowest_values(self.individuals, 1)
        return fittest[0]

    #DONE
    #Appends Individual instance into a Population instance's individuals attribute
    def add_individual(self, individual):
        if individual.chromosome_size != self.individual_size:
            raise AttributeError("Cannot add an individual of size {} in a population of individuals with size {}. Sizes must be the same.".format(individual.chromosome_size, self.individual_size))
        elif len(self.individuals) == self.population_size:
            raise AttributeError("Cannot add an individual to the population if the population size has reached its maximum capacity. Maximum population capacity: {}.".format(self.population_size))
        else:
            self.individuals.append(individual)

    #DONE
    #Appends many Individual instances (list) into a Population instance's 'individuals' attribute
    def add_individuals(self, individuals: list, *size_check):
        if size_check:
            for individual in individuals:
                if individual.chromosome_size != self.individual_size:
                    raise AttributeError("Sizes of all individuals to add to population must be the same as the the individuals in the population, i.e. {}. Individual with size {} was found in 'individuals' collection.".format(self.individual_size, individual.chromosome_size))
        if (len(self.individuals) + len(individuals)) > self.population_size:
            raise AttributeError("Cannot add a group of individuals to the population if the population size surpasses its maximum capacity after addition. Maximum population capacity: {}. Remaining space of population: {}. Amount of individuals to add to to the population: {}.".format(self.population_size,self.population_size - len(self.individuals) ,len(individuals)))
        else:
            for individual in individuals:
                self.add_individual(individual)    
    
    #DONE
    #Sets Population's population_size and individual_size static variables [AUXILIARY]
    @staticmethod
    def set_size(*sizes: tuple):
        if len(sizes) <= 0 or len(sizes) > 2:
            raise TypeError("Population set_size() function expects 1 or 2 arguments, {} given.".format(len(sizes)))
        elif len(sizes) > 0:
            Population.population_size = sizes[0]
            if len(sizes) == 2:
                Population.individual_size = sizes[1]

    #DONE
    #Reset static variables of class [AUXILIARY]
    @staticmethod
    def reset_population_class():
        Population.generation = 0
        Population.set_size(0, 0)
        Population.elite_portion = 0.0
        Population.mutant_portion = 0.0

    #DONE
    #Set elite portion
    @staticmethod
    def set_elite_portion(portion: float):
        if not (isinstance(portion, float) or isinstance(portion, int)):
            raise TypeError("Passed 'portion' argument must be a numeric value ('float' or 'int'). Passed argument is of type: {}.".format(type(portion)))
        elif portion < 0.0 or portion > 1.0:
            raise ValueError("Passed argument 'portion' must be no less than 0.0 and no more than 1.0 [0.0, 1.0]. Passed argument is {}.".format(portion))
        elif (portion + Population.mutant_portion) > 1.0:
            raise AttributeError("The given elite portion and current mutant portion must not add up more than 1.0. Given elite portion and current mutant portions are {} & {}, respectively.".format(portion, Population.mutant_portion))
        Population.elite_portion = float(portion)
    
    #DONE
    #Set mutant portion
    @staticmethod
    def set_mutant_portion(portion: float):
        if not (isinstance(portion, float) or isinstance(portion, int)):
            raise TypeError("Passed 'portion' argument must be a numeric value ('float' or 'int'). Passed argument is of type: {}.".format(type(portion)))
        elif portion < 0.0 or portion > 1.0:
            raise ValueError("Passed argument 'portion' must be no less than than 0.0 and no more than 1.0 [0.0, 1.0]. Passed argument is {}.".format(portion))
        elif (portion + Population.elite_portion) > 1.0:
            raise AttributeError("The given mutant portion and current elite portion must not add up more than 1.0. Given mutant portion and current elite portions are {} & {}, respectively.".format(portion, Population.elite_portion))
        Population.mutant_portion = float(portion)

    #DONE
    #Set portions
    @staticmethod
    def set_portions(elite_portion, mutant_portion):
        if not ((isinstance(elite_portion, float) or isinstance(elite_portion, int)) and (isinstance(mutant_portion, float) or isinstance(mutant_portion, int))):
            print('invalid arguments')
            raise TypeError("Passed arguments 'elite_portion' and 'mutant_portion' must be both of type 'float'. Passed argument are of {} and {}, respectively.".format(type(elite_portion), type(mutant_portion)))
        elif (elite_portion < 0.0 or mutant_portion > 1.0) or (mutant_portion < 0.0 or mutant_portion > 1.0):
            raise ValueError("Passed arguments 'elite_portion' and 'mutant_portion' must both be no less than 0.0 and no more than 1.0 [0.0, 1.0]. Given arguments are {} & {}.".format(elite_portion, mutant_portion))
        elif (elite_portion + mutant_portion) > 1.0:
            raise AttributeError("Given 'elite_portion' and 'mutant_portion' arguments must add up no more than 1.0. Given portions add up to {}.".format(elite_portion + mutant_portion))
        Population.elite_portion = float(elite_portion)
        Population.mutant_portion = float(mutant_portion)
    
    #-------------------------Printers-------------------------

    #DONE
    #Auxiliary individuals pretty printer [AUXILIARY]
    def print_individuals(self):
        print("Individuals:")
        if not self.individuals:
            print("None")
        else:
            for individual in self.individuals:
                print(individual.chromosome)

    #DONE
    #Auxiliary elite individuals pretty printer [AUXILIARY]
    def print_elite(self):
        print("Elite:")
        if not self.elite_individuals:
            print("None")
        else:
            for individual in self.elite_individuals:
                print(individual.chromosome)

    #DONE
    #Auxiliary non-elite individuals pretty printer [AUXILIARY]
    def print_non_elite(self):
        print("Non-Elite:")
        if not self.non_elite_individuals:
            print("None")
        else:
            for individual in self.non_elite_individuals:
                print(individual.chromosome)
        
    #DONE
    #Auxiliary printer for class attributes
    @staticmethod
    def print_population_class():
        print("-------------------------")
        print("    Population Class:")
        print("Class generation counter: ", Population.generation)
        print("Class population size: ", Population.population_size)
        print("Class individual size: ", Population.individual_size)
        print("Elite portion: ", Population.elite_portion)
        print("Mutant portion: ", Population.mutant_portion)
        print("-------------------------")

    #DONE
    #Auxiliary population pretty printer [AUXILIARY]
    def print_population(self):
        print("-------------------------")
        print("    Population:")
        self.print_individuals()
        print("Class generation counter: ", Population.generation)
        print("Instance generation: ", self.generation)
        print("Class population size: ", Population.population_size)
        print("Instance population size: ", self.population_size)
        print("Class individual size: ", Population.individual_size)
        print("Instance individual size: ", self.individual_size)
        print("Elite portion: ", Population.elite_portion)
        self.print_elite()
        self.print_non_elite()
        print("Mutant portion: ", Population.mutant_portion)
        print("-------------------------")

#MAIN
def main():
    p = Population(5,3)
    p.create_random_population()
    Population.set_elite_portion(0.3)
    p.individuals[0].quality = 1
    p.individuals[1].quality = 32
    p.individuals[2].quality = 23
    p.individuals[3].quality = 0
    p.individuals[4].quality = 12
    p.print_individuals()
    p.sort_individuals()
    p.print_individuals()
    p.print_population()
    p.classify_population()
    p.print_population()
    child = p.crossover(0.7)
    print(child.chromosome)
    print(p.get_average_fitness())
    print(p.get_average_elite_fitness())
    fittest = p.get_fittest_individual()
    fittest.print_individual()
    
if __name__ == '__main__':
    main()
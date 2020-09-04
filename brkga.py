from os import walk
from os import path
from time import time
import data_file
import population
import decoder as Decoder

'''
- MAIN or BRKGA LAYOUT:
    - ASK for user input arguments (g:generations, size: population size, )
    NOTE: Keep track of all populations in list-like structure
    - CREATE first population
        Use: Population.Population()
    - [Optional] CREATE data files before using the Decoder
    - In FOR or WHILE loop start BRKGA (conditions for stopping or breaking are the problem's stopping rules)
    - ITERATE Individuals list of Individual objects
        - Pass each Individual to the Decoder
        - Assign the resulting (calculated) quality/fitness to each Individual 
            (TODO: CHECK if assingment can be done in the Decoder)
            (CHECK if Decoder instances are needed or better use the module as a Static or Abstract class (or Module))
    - TODO: SORT the Individuals list  with the Population.sort() method based on the quality attribute
        (Implement sorting. NOTE: Sorting is done from lowest to greatest quality or 'total cost')
    - TODO: CLASSIFY Individuals list in Elite and Non-elite based on Population's attribute Elite.
        (TODO: USE seperate list as an attribute of Population class to store the Elite individuals)
            TODO: Create method for Population instances to store Elites
    - CHECK Stopping 


NOTE: CREATE separate script that creates the data files and calls the BRKGA main function
'''

class Brkga:

    chromosome_size = 0
    population_size = 0
    directory_path = 'data'
    generations = 0
    elite_portion = 0.0
    mutant_portion = 0.0
    inheritance_probability = 0.7

    #CREATES problem data in directory (specified by the 'directory_path' static var) by requesting user inputs (ranges) for random generation
    @staticmethod
    def create_data(use_current_data = True):
        '''
        CHECK if data is found in dir
            SET flag
        IF flag is TRUE
            ASK user if would like to use existing data
            set flag2
        IF NOT flag2
            (CREATE data with user inputs)
            ASK for amount of enitities/type of facilities
            (SAVE in int var)
            FOR amount:
                ASK for NAMES of entities in the supply chain order
                    (ASK for the demander or end type at the end)
                (SAVE in dynamic struct, e.g. array, list, dict [preferable])
                ASK for AMOUNT of facilities for the entity type
                (SAVE in dynamic struct, e.g. array, list, dict [preferable])
                ASK for PRODUCT range
                ASK for OPENING_COST range
                IF the entity type is NOT the end type (demander)
                    ASK for TRANSPORTATION_COST range
                SAVE in dict struct
            CHECK problem viability with 'data_file' module func [PENDING implementation]
            CALL generate_data from 'data_file' module [PENDING implementation]
        '''
        pass

    #DONE
    #REQUEST BRKGA run parameters
    @staticmethod
    def request_parameters():
        print("")
        print("BRKGA parameters:")
        print("")

        #INPUTS

        #GENERATIONS
        _required_type = type(Brkga.generations)
        generations = None
        try:
            generations = input("Number of generations? ")
            generations = int(generations)
        except:
            raise ValueError("Please provide a valid type for the the 'generations' parameter. Expected type: {}. Provided value: {}.".format(_required_type, generations))
        Brkga.generations = generations

        #CHROMOSME SIZE
        if path.exists(Brkga.directory_path):
            Brkga.set_chromosome_size()
        else:
            raise OSError("{} directory does not exist. Please verify data has been created in the specified directory before running the program.".format(Brkga.directory_path))

        #POPULATION SIZE
        _required_type = type(Brkga.population_size)
        poputlation_size = None
        input_counter = 0
        try:
            answer_set = ["Y", "y", "N", "n"]
            answer = None
            while not answer in answer_set and input_counter < 3:
                answer = input("Use default population size? (Y/N) ")
                input_counter += 1
                if answer == "N" or answer == "n":
                    population_size = input("Population size? ")
                    population_size = int(population_size)
                    input_counter = 0
                elif answer == "Y" or answer == "y":
                    Brkga.set_population_size()
                    population_size = None
                    input_counter = 0
        except:
            raise ValueError("Please provide a valid type for the the 'population size' parameter. Expected type: {}. Provided value: {}.".format(_required_type, population_size))
        if input_counter == 3:
            raise ValueError("Execution terminated due to conitnous input of invalid parameters.")
        elif population_size:
            Brkga.population_size = population_size

        #ELITE PORTION
        _required_type = type(Brkga.elite_portion)
        elite_portion = None
        try:
            elite_portion = input("Elite portion [0.0, 1.0]? ")
            elite_portion = float(elite_portion)
        except:
            #raise ValueError("Please provide a valid type for the the 'elite portion' parameter. Expected type: {}. Provided value: {}.".format(_required_type, elite_portion))
            pass
        if elite_portion <= 1.0 and elite_portion >= 0.0:
            Brkga.elite_portion = elite_portion
        else:
            raise ValueError("Please provide a float type (or integer) value in between [0.0, 1.0]. Provided value is: {}.".format(elite_portion))

        #MUTANT PORTION
        _required_type = type(Brkga.mutant_portion)
        mutant_portion = None
        try:
            mutant_portion = input("Mutant portion [0.0, {}]? ".format(1.0 - elite_portion))
            mutant_portion = float(mutant_portion)
        except:
            raise ValueError("Please provide a valid type for the the 'mutant portion' parameter. Expected type: {}. Provided value: {}.".format(_required_type, mutant_portion))
        if (mutant_portion + Brkga.elite_portion) <= 1.0:
            Brkga.mutant_portion = mutant_portion
        else:
            raise ValueError("Please provide a float type (or integer) value in between [0.0, {}]. Provided value is: {}.".format(1.0 - Brkga.elite_portion, mutant_portion))

        #ELITE INHERITANCE PROBABILITY
        _required_type = type(Brkga.inheritance_probability)
        inheritance_probability = None
        try:
            inheritance_probability = input("Elite allele inheritance probability [0.0, 1.0]? ")
            inheritance_probability = float(elite_portion)
        except:
            raise ValueError("Please provide a valid type for the the 'elite allele inheritance probability' parameter. Expected type: {}. Provided value: {}.".format(_required_type, inheritance_probability))
        if inheritance_probability > 0.0 and inheritance_probability < 1.0:
            Brkga.elite_portion = elite_portion
        else:
            raise ValueError("Please provide a float type (or integer) value in between [0.0, 1.0]. Provided value is: {}.".format(inheritance_probability))

    #DONE
    #GET chromosome size based on current data in the 'directory_path' path 
    @staticmethod
    def set_chromosome_size():
        size = 0
        #ITERATE over each directory and its files under the ''directory_path'/entities' dir
        for directory, subdirectory, files in walk(path.join(Brkga.directory_path, 'entities')):
            for _file in files:
                #CALUCULATE size by counting the lines of each file pertaining entity data
                size += data_file.count_lines(_file, directory)
        #SET the DEFAULT chromosome_size defined by: size = |I| + |J| + |K|
        Brkga.chromosome_size = size
        return size

    #DONE
    #SET DEFAULT population size based on the current chromosome size
    @staticmethod
    def set_population_size():
        Brkga.population_size = Brkga.chromosome_size*4
        return Brkga.population_size

    #RUN the BRKGA algorithm (cycle with the given parameters)
    @staticmethod
    def run():
        #Results from BRKGA run
        result = dict()
        #Don't do anything if the generation number is less or equal to zero
        if Brkga.generations <= 0:
            result['fittest'] = None
            result['quality'] = None
            result['avg. elite fitness'] = None
            result['time'] = 0.0
            return result
        #Genertation counter
        generations = 1
        #Last generation after whole evolutionary process
        last_population = None
        #SET the Population class static (or class) attributes with the corresponing parameters
        population.Population.set_size(Brkga.population_size, Brkga.chromosome_size)
        population.Population.set_portions(Brkga.elite_portion, Brkga.mutant_portion)
        #PREPARE decoder
        decoder = Decoder.Decoder()
        decoder.load_data()
        #START timer
        start = time()
        #CREATE first population
        first_population = population.Population()
        first_population.create_random_population()
        #DECODE each individual in the first population, calulate its quality/fitness value and assign it to the individual's attribute
        for individual in first_population.individuals:
            individual.quality = decoder.decode(individual.chromosome)
        #-----REMOVE-----
        print('UNSORTED')
        for individual in first_population.individuals:
            print(individual, ': ',individual.quality)
        #----------------
        #SORT population based on the individual's quality
        first_population.sort_individuals()
        #-----REMOVE-----
        print('SORTED', end="\n")
        for individual in first_population.individuals:
            print(individual, ': ',individual.quality)
        #----------------
        #CLASSIFY population in elite and non-elite
        first_population.classify_population()
        #-----REMOVE-----
        print('ELITE: ')
        for individual in first_population.elite_individuals:
            print(individual.quality)
        print('NON-ELITE: ')
        for individual in first_population.non_elite_individuals:
            print(individual.quality)
        #----------------
        #START evolutionary process based on the given number of generations
        previous_population = first_population
        #-----REMOVE-----
        print('Generation {}'.format(generations))
        for individual in previous_population.individuals:
            print(individual, ': ', individual.quality)
        #ASSIGN the first population to the last in case the generations are only 1
        last_population = first_population
        #----------------
        while generations < Brkga.generations:
            #COPY elite portion from the current (previous) population to next population
            next_population = population.Population()
            #TODO: REMOVE size check in add_individuals call
            next_population.add_individuals(previous_population.elite_individuals, True)
            #ADD mutants to the next population
            mutants = population.Population()
            #TODO: [OPTIONAL] CREATE population instance method to generate mutants (random) individuals in population
            mutants.create_random_population(Brkga.mutant_portion)
            next_population.add_individuals(mutants.individuals, True)
            #PERFORM the crossover to complete the missing/remaining portion of the population
            for _ in range(next_population.population_size - len(next_population.individuals)):
                offspring = previous_population.crossover(Brkga.inheritance_probability)
                next_population.add_individual(offspring)
            #DECODE the the individuals that haven't been decoded in the new population
            for individual in next_population.individuals:
                if not individual.quality:
                    individual.quality = decoder.decode(individual.chromosome)
            #SORT new population based on the individual's quality
            next_population.sort_individuals()
            #CLASSIFY population in elite and non-elite
            next_population.classify_population()
            #-----REMOVE-----
            print('Generation {}'.format(generations + 1))
            for individual in next_population.individuals:
                print(individual, ': ', individual.quality)
            #----------------
            generations += 1
            if generations == Brkga.generations:
                last_population = next_population
            else:
                previous_population = next_population
        #END timer
        end = time()
        result['fittest'] = last_population.get_fittest_individual()
        result['quality'] = result['fittest'].quality
        result['avg. elite fitness'] = last_population.get_average_elite_fitness()
        result['time'] = end - start
        return result   

    #PRETTY PRINTER for the BRKGA parameters
    def print_parameters():
        print("Directory path: ", Brkga.directory_path)
        print("Chromosome size: ", Brkga.chromosome_size)
        print("Population size: ", Brkga.population_size)
        print("Genertations: ", Brkga.generations)
        print("Elite portion: ", Brkga.elite_portion)
        print("Mutant portion: ", Brkga.mutant_portion)
        print("Inheritance probability ", Brkga.inheritance_probability)

#MAIN
def main():
    Brkga.request_parameters()
    result = Brkga.run()
    print(result)


if __name__ == '__main__':
    main()

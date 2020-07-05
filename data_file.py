from random import Random
import os

'''
TODO LIST:
+ REDO: check_range_viability(...)
+ CORRECT create_faciliites(...) -> which works as the main function
+ ADD module documentation

- Look into yaml files for data storage

+ Check if converting module into class is useful
    - if so, have a default and settable attribute for the data directory


#NOTE: when having optional params in functions have a default for it defined in the function.
'''

#TODO: Add documentation for module
"""Data File Module for generating solvable LIPO problems through data generated in *.txt files.
"""

#---DONE---
def create_entity(name: str, number: int, product_range: tuple, opening_cost_range: tuple, *directory_path: str):
    """Creates an entity text file in the specified directory with the given entity (or facility type) data.
    
    Creates an entity text file (*.txt) with the given name and specified parameters for number of facilites, opening cost 
    ranges and demand or capacity of products ranges. Checks if the specified directory exists beforehand (if not, it's created)
    and creates the text file with pseudo-randomly selected data for the given ranges, specified facility type name and number of 
    facilities for the entity in it. The resulting text file descibes the capacity/demand and opening cost for each facility. 
    Each row in the file represents a distinct facility of the same type. The total amount of rows in the resulting file should
    be equal to the number parameter. The first column in the text file represents all demands/capacities for each facility. The 
    second column in the text file represents all opening costs for each facility.

    Args: 
        name: Name (String) for the entity or facility type to create (used for the name of the text file).
        number: Number (Integer) of facilities that will be represented in the generated text file.
        product_range: Ranges (Integer duple) used to define pseudo-randomly the amount products a facility can hold (i.e. 
            demand or capacity).
        opening_cost_range: Ranges (Float duple) used to define pseudo-randomly the opening cost for a given facility.
        *directory_path: The directory path (String) were to create the entity text file. This parameter is optional. In case no
            directory_path argument is provided, the default value will be the './data' directory path.

    Returns:
        maximum_products: The sum or total amount of products all facilities in the text file can hold together (i.e. the 
            maximum capacity or demand that all facilities of the same type can have altogether).

    Raises:
        ValueError: If the number, product_range, or opening_cost_range passed arguments contain inappropriate values for the 
            entity text file generation.
        TypeError: If the the passed directory_path argument is not valid. Raised if a single String argument is not passed.
    """
    #Argument validation
    if number <= 0:
        raise ValueError("Passed 'number' argument (arg[1]) must be greater than 0. {} was provided as argument.".format(number))
    elif product_range[0] > product_range[1]:
        raise ValueError("In passed 'product_range' argument (arg[2]), lower bound value must be smaller than upper bound value. {} was provided as argument.".format(product_range))
    elif product_range[0] <= 0 or product_range[1] <= 0:
        raise ValueError("In passed 'product_range' argument (arg[2]), upper and lower bound of range must be greater than 0. {} was provided as argument.".format(product_range))
    elif opening_cost_range[0] > opening_cost_range[1]:
        raise ValueError("In passed 'opening_cost_range' argument (arg[3]), lower bound value must be smaller than upper bound value. {} was provided as argument.".format(opening_cost_range))
    elif opening_cost_range[0] < 0 or opening_cost_range[1] < 0:
        raise ValueError("In passed 'opening_cost_range' argument (arg[3]), upper and lower bound of range must be positive values. {} was provided as argument.".format(opening_cost_range))
    elif directory_path and (len(directory_path) > 1 or not isinstance(directory_path[0], str)):
        raise TypeError("Passed 'directory_path' argument (arg[4]) is not valid. Only a single String argument is needed if passed. {} was provided as argument.".format(directory_path))
    #Default directory path
    path = 'data'
    if directory_path: #True if directory_path is passed as argument
        path = directory_path[0]
    #File generation
    maximum_products = 0
    if not os.path.exists(path): #True if the directory were files are to be created doesn't exist.
        os.mkdir(path)
    file_name = name + '.txt'
    with open(os.path.join(path, file_name), 'w') as entity_file:
        for i in range(number):
            #Range: random int between a and b where [a, b]
            number_products = Random().randint(product_range[0], product_range[1])
            maximum_products += number_products
            #Range: random float between a and b where [a, b]
            cost = Random().uniform(opening_cost_range[0], opening_cost_range[1])
            entity_file.write(str(number_products) + ' ' + str(cost) + '\n')
        entity_file.close()
    return maximum_products

#---DONE---
def define_transporation(*directory_path: str, **cost_ranges: dict):
    """Creates a text file in the specified directory defining the transportation cost of a product between two distinct 
    facilities.
    
    Creates a text file (*.txt) containing the trasportation costs for all facilites specified by the entity text files in the
    same directory. The usage of this function must be done considering that entity text files have already been created through
    the 'create_entity' function.The produced file is named 'transportation.txt' and defines the cost for trasportation between 
    different facilities using coulmuns. The first column corresponds to the facility from which the product is sent (i.e. the 
    supplier), the second column corresponds to the facility which recieves the prouduct (i.e the demander or client), and the 
    third column corresponds to the cost of transporting a single unit of prouduct from the supplier facility to the demander 
    facility. Note that the generation of the 'transportation.txt' file follows the rule of one way transportation, meaning that 
    products are only transported from the supplier facility to the demander facility.

    Args:
        *directory_path: The directory path (String) were to create the the 'transportation.txt' text file. This parameter is 
            optional. In case no directory_path argument is provided, the default value will be the './data' directory path.
        **cost_ranges: A structure (dict of key (String) and value (duple) pairs) which contains the cost ranges from which each
            transportation cost will be defined pseudo-randomly based on the facilites defined in their corresponding entity 
            files. The last cost range corresponding to the last facility in the supply chain (represented as the last key in the 
            structure) is not considered for the random generation (This may be taken as None or any other value). Note that the 
            keys in the structures must contain the exact names as the the entity text files (exculding the exenxion *.txt). A 
            **cost_ranges argument examples:
            
            **{'plant': (21.3, 123.23), 
               'depot': (38.3, 48.3), 
               'client': None}

            enitity1 = (122.05, 134.98), 
            enitity2 = (12.0, 22.2), 
            enitity3 = (0, 0)

    Returns:
        Nothing is returned.

    Raises:
        TypeError: An error is raised if the wrong amount of argunments is passed in to the function.
        ValueError: An error is raised if the passed in arguments are not appropriate for the 'transportation.txt' text file 
            generation.
        OSError: An error occured for not being able to find the specified directory, meaning that no enitity text files were 
            found either.

    Typical usage example:

        define_transporation('data', **{'plant': (21.3, 123.23), 'depot': (38.3, 340.3), 'client': None})
        define_transporation('someDirectory', plant = (21.3, 123.23), depot = (38.3, 340.3), client = None)
    """
    #Argument validation for *directory_path
    if directory_path and (len(directory_path) > 1 or not isinstance(directory_path[0], str)):
        raise TypeError("Passed 'directory_path' argument (arg[4]) is not valid. Only a single String argument is needed if passed. {} was provided as argument.".format(directory_path))
    #Default directory path
    path = 'data'
    if directory_path: #True if directory_path is passed as argument
        path = directory_path[0]
    #Diretory existence check
        if not os.path.exists(path):
            raise OSError("'{}' directory, which should contain the entity text files, hasn't been created. Make sure to create the directory with the appropriate files beforehand.".format('./' + path))
    #Argument validation for **cost_ranges
    for key, value in cost_ranges.items():
        full_path = os.path.join(path, key + '.txt')
        if not (os.path.exists(full_path) and os.path.isfile(full_path)):
            raise ValueError("No entity with the '{}' name matches any text file in the './{}' directory. A corresponding text file with '{}.txt' name should exist in the directory. Please check directory or entity names in passed arguments.".format(key, path, key))
        elif value[0] > value[1]:
            raise ValueError("In passed '**cost_ranges' argument (arg[1]), lower bound value must be smaller than upper bound value for the entity's cost range. Entity's cost range error was for '{}' -> {}.".format(key, value))
        elif value[0] <= 0 or value[1] <= 0:
            raise ValueError("In passed '**cost_ranges' argument (arg[1]), upper and lower bound of cost ranges must be greater than 0. Entity's cost range error was for '{}' -> {}.".format(key, value))
    #File generation
    try:
        transportation_file = open(os.path.join(path, 'transportation.txt'), 'w')
    except(FileNotFoundError):
        raise OSError("'{}' directory, which should contain the entity text files, hasn't been created. Make sure to create the directory with the appropriate files beforehand.".format('./' + path))
    entities = list()
    for entity in cost_ranges:
        entities.append((entity, count_lines(entity + '.txt')))
    #Example of resulting entities list after previous for loop: [('entity1', 3), ('entity2', 2), ('entity3', 5)]
    count = 0
    for entity1, number1 in entities:
        if count < len(entities) - 1: #True if entity1 is not the last entity of the entities list
            for index1 in range(1, number1 + 1):
                entity2 = entities[count + 1][0]
                number2 = entities[count + 1][1]
                for index2 in range(1, number2 + 1):
                    cost = Random().uniform(cost_ranges[entity1][0], cost_ranges[entity1][1])
                    transportation_file.write(entity1 + str(index1) + ' ' + entity2 + str(index2) + ' ' + str(cost) + '\n')
        count += 1
    transportation_file.close()

#---DONE---
def count_lines(file_name: str, *directory_path: str): 
    """Counts lines in a specific file in a specific directory.

    This function is an AUXILIARY function, meaning its use is only meant for other functions in this module. It counts the 
    lines in a text file (*.txt) to know the amount of certain type of facilities (e.g. client, depot, plant, etc.) that are 
    represented by the file itself. The amount of lines in a file represent the amount of facilities for the corresponding type
    (e.g. if 'client.txt' has 3 lines, there are 3 clients represented). To use correclty, files with their corresponding entity
    names must be already created. Trying to count lines of non-existent files result in an exception.
    
    Args:
        file_name: A text file (*.txt) name (String).
        *directory_path: The directory path (String) were to find the file to count its lines. This parameter is optional. In 
            case no directory_path argument is provided, the default value will be the './data' directory path.

    Returns:
        count: The number (Integer) of lines in a file with the corresponding file name.

    Raises:
        TypeError: If the the passed directory_path argument is not valid. Raised if a single String argument is not passed.
        OSError: An error occured for not being able to find the indicated text file through the passed file name and directory 
            path.
    """
    #Argument validation
    if directory_path and (len(directory_path) > 1 or not isinstance(directory_path[0], str)):
        raise TypeError("Passed 'directory_path' argument (arg[4]) is not valid. Only a single String argument is needed if passed. {} was provided as argument.".format(directory_path))
    #Default directory path
    path = 'data'
    if directory_path: #True if directory_path is passed as argument
        path = directory_path[0]
    #Try and open file with the specified directory path and file name
    try:
        file = open(os.path.join(path, file_name), 'r')
    except(FileNotFoundError):
        raise OSError("File with name '{}' could not be found in the {} directory. Please check the passed file name and directory path".format(file_name, path))
    count = 0
    for line in file:
        count += 1
    file.close()
    return count

#X---DONE---
#Check the viability of ranges (product enitity amounts) and number of entities for a given sovable LIPO problem [AUXILIARY]
#A probability check is done given by the amount of entities there can posibly be multiplied by the probability that a randomly selected number (representing the amount of products an enitity can hold) belongs or not to given overlapping ranges.
def check_range_viability(range1: tuple, range2: tuple, number1: int, number2: int):
    probability1 = 100.0
    probability2 = 100.0
    if range2[0] < range1[1] <= range2[1]:
        probability1 = (range1[1] - range2[0]) / (range1[1] - range1[0])
        probability2 = (range2[1] - range1[1]) / (range2[1] - range2[0])
    elif range1[0] < range2[1] <= range1[1]:
        probability1 = (range1[1] - range2[1]) / (range1[1] - range1[0])
        probability2 = (range2[1] - range1[0]) / (range2[1] - range2[0])

    #CHECK for non overlapping ranges
    #Probability check...
    if (probability1 * number1) >= (probability2 * number2):
        return True
    else:
        return False

'''
#Creates a valid, solvable problem for a LIPO approach solution.
def create_facilities(*args: list):
    #Example of *args param: ['plant', 4, (50, 60), (876.00, 4563.00), (93.0, 122.95), 'depot', 3, (40, 50), (324.00, 2341.00), (54.3, 543.00), 'client', 5, (30, 40), None, None]

    #Argument assignment
    args_per_entity = 5 #Arguments per entity
    number_of_entites = int(len(args)/args_per_entity) #Number of types of entities
    entities = list()
    numbers = list()
    product_ranges = list()
    opening_cost_ranges = list()
    transportation_costs_ranges = list()
    maximum_products = 0
    valid_problem = True
    for i in range(len(args)):
        remainder = i % args_per_entity
        if remainder == 0:
            entities.append(args[i])
        elif remainder == 1:
            numbers.append(args[i])
        elif remainder == 2:
            product_ranges.append(args[i])
        elif remainder == 3:
            opening_cost_ranges.append(args[i])
        elif remainder == 4:
            transportation_costs_ranges.append(args[i])

    for j in range(number_of_entites-1):
        print(check_range_viability(product_ranges[j], product_ranges[j + 1], numbers[j], numbers[j + 1]))
        if not check_range_viability(product_ranges[j], product_ranges[j + 1], numbers[j], numbers[j + 1]):
            raise ValueError("Product ranges provided are highly unlikely to produce a solvable problem.")

    maximum_products = create_entity(entities[-1], numbers[-1], product_ranges[-1], opening_cost_ranges[-1])
    for k in range(number_of_entites - 2, -1, -1):
        possible_maximum = create_entity(entities[k], numbers[k], product_ranges[k], opening_cost_ranges[k])
        while maximum_products > possible_maximum:
            possible_maximum = create_entity(entities[k], numbers[k], product_ranges[k], opening_cost_ranges[k])
        maximum_products = possible_maximum
'''

#MAIN
def main():
    #print(check_range_viability((50, 60), (40, 50), 4, 3))
    #print(check_range_viability((40, 50), (30, 40), 3, 5))
    #create_facilities('plant', 4, (50, 60), (876.00, 4563.00), (93.0, 122.95), 'depot', 3, (40, 50), (324.00, 2341.00), (54.3, 543.00), 'client', 5, (30, 40), (0,0), None)
    
    entity1 = 'plant'
    entity2 = 'depot'
    entity3 = 'client'
    print(create_entity(entity1, 4, (23, 34), (12.2, 33.5)))
    print(create_entity(entity2, 2, (23, 34), (12.2, 33.5)))
    print(create_entity(entity3, 3, (23, 34), (12.2, 33.5)))

    define_transporation(plant = (21.3, 123.23), depot = (38.3, 340.3), client = (0,0))
    '''
    transportation_costs = {entity1: (21.3, 123.23), entity2: (38.3, 340.3), entity3: None} 
    define_transporation(**transportation_costs)
    '''

if __name__ == '__main__':
    main()
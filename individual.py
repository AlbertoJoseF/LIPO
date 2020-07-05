from random import Random
from functools import total_ordering


'''
TODO:

- Check and implement were to type check
    - Make the code as re-usable as possible
        - Look into try-catch blocks -> Duck typing (increases usability)
        - Implement functions dedicated to type and value checking (for usage in constructors and class methods)
        - Having variable checks for objects which are based on how Primitive data types or native classes work.
            - If the focus on handling primitive type is done, the usage is greater.
            - Later, what is to be focused on is adapting complex types (classes) to work as the primitive types or native classes
              so that they are compatible

- Stick to the private attributes syntax, e.g. _var = 'value'

- Document code (Docstrings)
'''

#Individual class
@total_ordering
class Individual:
    #Individual chromosome (key-value vector) size
    chromosome_size = 0
    #Random instance for generating and mutating Individual chromosomes
    random_instance = Random()

    #Contructor / Initializer
    def __init__(self, *arg: tuple):

        #Key-value vector
        self.chromosome = list()

        #Chromosome size
        self.chromosome_size = 0
        
        #Quality of individual
        self.quality = 0 

        #Set static Class size variable if provided in constructor call (*size)
        if len(arg) > 1:
            raise TypeError("Individual __init__() constructor expects 0 or 1 argument, {} given.".format(len(arg)))
        elif len(arg) > 0:
            if isinstance(arg[0], list):
                self.chromosome = arg[0]
                self.chromosome_size = len(self.chromosome)
            elif isinstance(arg[0], int):
                self.chromosome_size = arg[0]
            else:
                raise TypeError("Passed argument must be 'int' or 'list' type. Provided argument is of type: {}.".format(type(arg[0])))
        else:
            self.chromosome_size = Individual.chromosome_size
        
        #If 'chromosome' argument is not passed or 'chromosome' attribute is an empty list, initialize the Individual's chromosome with random values between 0 and 1 -> [0.0, 1.0)
        if len(self.chromosome) == 0:
            for i in range(self.chromosome_size):
                self.chromosome.append(Individual.random_instance.random())

    #For sorting and comparison purposes
    def __lt__(self, other):
        return (self.quality < other.quality)
    
    def __gt__(self, other):
        return (self.quality > other.quality)

    def __le__(self, other):
        return (self.quality <= other.quality)

    def __ge__(self, other):
        return (self.quality >= other.quality)

    #Set Individual static size variable
    @staticmethod
    def set_size(size: int):
        if not isinstance(size, int):
            raise TypeError("Provided 'size' argument must be of type 'int'. Passed argument is of type {}.".format(type(size)))
        Individual.chromosome_size = size
    
    #Re-initialize Individual instances's attributes
    def mutate(self):
        for i in range(len(self.chromosome)):
            self.chromosome[i] = Individual.random_instance.random()
        self.quality = 0

    #Auxiliary pretty printer [AUXILIARY]
    def print_individual(self):
        print("---Individual---")
        print("Individual instance size: ", self.chromosome_size)
        print("Individual class size: ", Individual.chromosome_size)
        print("Quality: ", self.quality)
        print("Chromosome:")
        print(self.chromosome)
        print("----------------")

#MAIN
def main():
    #Create Individual instances
    i = Individual(1)

    #Print all values for the Individual instance and class
    i.print_individual()
    
    #Create Individual instances
    Individual.set_size(5)
    i2 = Individual([0.2,0.1,0.2,0.2])

    #Print all values for the Individual instance and class
    i2.print_individual()

    i2.mutate()

    i2.print_individual()

    i3 = Individual(3)
    i3.quality = 4

    i4 = Individual(4)
    i4.quality = 5
    
    print(i4 < i3)


    i3.print_individual()

if __name__ == '__main__':
    main()
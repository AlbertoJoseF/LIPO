import os
from collections.abc import Iterable
from copy import deepcopy
from time import time

#Decoder class meant to calculate the fitness/quality of an individual's chromosome or vector
class Decoder:
    #Directory were output data is to be stores (e.g. transportation routes)
    _directory_path = 'data'
    #Export routes into text file flag
    _export_routes = False
    #Type and value argument check flag
    _argument_check = True

    #PRIVATE structures and data for treating problem data

    #Costs of transportation for a single product
    _transportation_costs = dict()
    #Costs for opening a facility/entity
    _openning_costs = dict()
    #Demands and Capacities of products
    _products = dict()
    #OPTIONAL??? Established supply direction
    _supply_direction = list()
    #Template for the vector-chromosome mapping loaded when load_data static function is excuted
    _vector_mapping = dict()
    #Template for the '_total_capacities' variable of any Decoder instance
    _total_capacities_default = dict()
    #Selection step treshold value
    _treshold = 0.5

    #DONE
    #Initializer
    def __init__(self, directory_path = None):
        #key-value vector for mapping the chromosome to the problem's (LIPO) solution representation
        self.vector = None
        #Quality of the passed chromosome (mapped into the 'vector' variable) and calculated through the 'decode function'. Also known as the calculated TOTAL COST for the given chromosome
        self.quality = 0
        #Total product capacity by each type to entity
        self._total_capacities = None
        #routes established for the given 'vector'
        self._routes = dict()
        #set the directory path if passed
        if directory_path:
            Decoder._directory_path = directory_path

    #DONE
    #Setter for the _directory_path static class variable
    @staticmethod
    def set_directory_path(directory_path: str):
        try:
            Decoder._directory_path = directory_path
        except: 
            raise ValueError("The received argument is in not valid. Please check. Passed param is: {}.".format(directory_path))

    #DONE
    #Loads data from the problem data directory (sets the _products, _openning_costs, and _transportation_costs static class variables)
    @staticmethod
    def load_data(directory_path = None):
        if directory_path:
            path = directory_path
        else:
            path = Decoder._directory_path
        #Reset static struct variables
        Decoder._transportation_costs.clear()
        Decoder._openning_costs.clear()
        Decoder._products.clear()
        Decoder._supply_direction.clear()
        Decoder._vector_mapping.clear()
        Decoder._total_capacities_default.clear()
        #Load transportation and entitis problem data
        Decoder.__load_enitites(path)
        Decoder.__load_transportation(path)

    #DONE
    #Loads the the relevant data concerning entities in the 'entities' direcotry to the _openning_costs, _products variables & _entities.
    def __load_enitites(directory_path: str):
        entites_path = os.path.join(directory_path, 'entities')
        for current_directory, subdirectories, files in os.walk(entites_path):
            for _file in files:
                entity_data = Decoder._read_file_by_line(_file, current_directory)
                entity_name = os.path.splitext(_file)[0]
                Decoder._total_capacities_default[entity_name] = 0
                #CHANGE
                Decoder._supply_direction.append(entity_name)
                for index, entity in enumerate(entity_data, start = 1):
                    #Classify raw data
                    entity = entity.split()
                    product_amount = int(entity[0])
                    openning_cost = float(entity[1])
                    indexed_enitity_name = entity_name + str(index)
                    #Vector mapping template '_vector_mapping' definition 
                    if not indexed_enitity_name in Decoder._vector_mapping:
                        Decoder._vector_mapping[indexed_enitity_name] = dict()
                    Decoder._vector_mapping[indexed_enitity_name]['value'] = None
                    Decoder._vector_mapping[indexed_enitity_name]['type'] = entity_name
                    if current_directory == os.path.join(entites_path, "end_node"):
                        Decoder._vector_mapping[indexed_enitity_name]['end'] = True
                        Decoder._vector_mapping[indexed_enitity_name]['selected'] = True
                    else:
                        Decoder._vector_mapping[indexed_enitity_name]['end'] = False
                        Decoder._vector_mapping[indexed_enitity_name]['selected'] = False
                    #Classified problem data storage
                    Decoder._products[indexed_enitity_name] = product_amount
                    Decoder._openning_costs[indexed_enitity_name] = openning_cost

    #DONE
    #Loads the the relevant data transportation costs in the 'entities' direcotry to the _transportation_costs variable.
    def __load_transportation(directory_path: str):
        transportation_path = os.path.join(directory_path, 'transportation')
        if len(os.listdir(transportation_path)) != 1 or not('transportation.txt' in os.listdir(transportation_path)):
            raise OSError("'{}/transportation' directory must contain a single text file named 'transportation.txt'. Please check.".format(directory_path))
        trasportation_data = Decoder._read_file_by_line('transportation.txt', transportation_path)
        for route in trasportation_data:
            route = route.split()
            supplier_entity = route[0]
            demander_entity = route[1]
            transportation_cost = float(route[2])
            if not supplier_entity in Decoder._transportation_costs:
                Decoder._transportation_costs[supplier_entity] = dict()
            Decoder._transportation_costs[supplier_entity][demander_entity] = transportation_cost

    #DONE
    #AUXILIARY - Reads a file in a specific directory and return a list of strings containing each line in it as a list item
    def _read_file_by_line(filename: str, directory_path: str):
        path = os.path.join(directory_path, filename)
        _file = open(path, 'r')
        result = _file.read().splitlines()
        _file.close()
        return result          

    #DONE
    #Calculates and returns the fitness of quality value of a given chromosome (Iterable type)
    def decode(self, chromosome: list, export_routes = None):
        #Check if passed chromosome argument is valid for decoding
        chromosome_lenght = len(chromosome)
        valid_chromosome_lenght = len(Decoder._vector_mapping)
        if chromosome_lenght != valid_chromosome_lenght:
            raise ValueError("Chromosome properties (size) should match loaded problem data. Provided chromosome's size is: {}, and problem data cannot be mapped correctly due to it. Chomosome size should be exacly: {}.".format(chromosome_lenght, valid_chromosome_lenght))
        #Set _export_routes flag if argument is passed
        if export_routes:
            Decoder._export_routes = export_routes
        #Load vector mapping template to Decoder instance's vector
        self.vector = deepcopy(Decoder._vector_mapping)
        #Map the chromosome to the Decoder's vector dictionary variable
        for index, key in enumerate(self.vector):
            self.vector[key]['value'] = chromosome[index]
        #Load the '_total_capacities_default' static variable to the Decoder instance's '_total_capacities' varible
        self._total_capacities = deepcopy(Decoder._total_capacities_default)

        #SORT the vector based on the 'value'
        self.__sort_vector()

        #SELECT the facilities based on the given chromosome and the given problem contraints
        self.__select()

        #VERIFY that the given selection is valid given the problem's contraints
        self.__verify()

        #REMOVE SUPREFLUOUS facilities from the given valid selection
        self.__remove_superfluous()

        #ESTABLISH ROUTES with the given selection
        self.__establish_routes()

        #REMAP (modify) the original chromosome with the resulting selection
        self.__remap_chromosome(chromosome)

        #CALCULATE QUALITY of the the selection
        return self.__calculate_quality()
        
    #DONE
    #Selects (turns the 'selected' value to True) the key-values in the Decoder instance's attribute, 'vector'.
    def __select(self, _type = None):
        #Return flag in case selection process is performfed successfuly or not
        selection_successful = None
        #First kind selection (select all with 'value' equal or grater than the fixed treshold and those which are end nodes and have not been selected)
        if not _type:
            for key, value in self.vector.items():
                if (value['end'] == False and value['value'] >= Decoder._treshold) or (value['end'] == True and value['selected'] == False):
                    value['selected'] = True
            selection_successful = self.vector
            #First capacity calculation
            self.__calculate_total_capacities()
        #Second kind selection (select the first entity which appears in the 'vector' that hasn't been selected and that belongs to the provided '_type')
        else:
            for key, value in self.vector.items():
                if value['type'] == _type and value['selected'] == False:
                    value['selected'] = True
                    if value['value'] < Decoder._treshold:
                        value['value'] = 1 - value['value']
                    self.__calculate_total_capacities(key)
                    selection_successful = key
                    break
        return selection_successful

    #DONE
    #Un-selects a facility form the Decoder instance's vector through the use of its key/name
    def __un_select(self, facility: 'str'):
        deselection_successful = None
        if self.vector[facility]['selected'] == True:
            self.vector[facility]['selected'] = False
            if self.vector[facility]['value'] >= Decoder._treshold:
                self.vector[facility]['value'] = 1 - self.vector[facility]['value']
            self.__calculate_total_capacities(facility, False)
            deselection_successful = facility
        return deselection_successful
    
    #DONE
    #Verifies that the demands are met for the selected facilities
    def __verify(self):
        selectable = True
        for index, demander_entity in reversed(list(enumerate(Decoder._supply_direction))):
            if index > 0:
                supplier_entity = Decoder._supply_direction[index - 1]
                while self._total_capacities[supplier_entity] < self._total_capacities[demander_entity] and selectable:
                    selectable = self.__select(supplier_entity)
            if not selectable:
                raise AttributeError("A valid selection is not possible based on the currently loaded problem data. Please check that the data represents a solvable problem.")

    #DONE
    #Removes or de-selects the facilities which may not be needed as 'selected' for a given valid solution (specified by te 'vector')
    def __remove_superfluous(self, sort_by_product = True):
        iteration_list = None
        #Removes (un-selects) facilities by least product demand or capacity
        if sort_by_product: 
            iteration_list = sorted(Decoder._products.items(), key = lambda item: item[1], reverse = True)
        #Removes (un-selects) facilities by index
        else:
            iteration_list = self.vector.items()
        for index, demander_entity in reversed(list(enumerate(Decoder._supply_direction))):
            #If the parent or first supplier is not taken as a demander entity (since parent suppliers have no suppliers)
            if index > 0:
                supplier_entity = Decoder._supply_direction[index - 1]
                #If removal is possible for given product demand/capacity of supplier and demander entities
                if self._total_capacities[supplier_entity] > self._total_capacities[demander_entity]:
                    for key, value in iteration_list:
                        #Facility matches the supplier entity type and it has been selected in the 'vector'
                        if self.vector[key]['type'] == supplier_entity and self.vector[key]['selected'] == True:
                            #If removal is possible while taking into account that the supplier entity can still supply the demander entity
                            if self._total_capacities[supplier_entity] - Decoder._products[key] >= self._total_capacities[demander_entity]:
                                #Remove facility with given 'key' or name
                                self.__un_select(key)
                            #If further removal is not possible, stop iteration for given entity type
                            if self._total_capacities[supplier_entity] == self._total_capacities[demander_entity]:
                                break
                else:#No removal is possible for given entity type
                    break
            else:#The parent supplier or first supplier in supply chain is taken into account (and has no supplier to it)
                break

    #DONE - PENDING -> DOUBT: how to remap (modify) the original chromosome with the current vector??
    #Remaps back the given chromosome with the resulting 'vector'
    def __remap_chromosome(self, chromosome, original_order = True):
        mapping = self.vector
        #Optional case for remapping (maintaing order of the original chromosome)
        if original_order:
            mapping = Decoder._vector_mapping
        for index, key in enumerate(mapping):
            chromosome[index] = self.vector[key]['value']
        return chromosome

    #DONE
    #Calculates the total cost of quality for the current vector and routes selection (specified in the intance's 'vector' and '_routes' variables)
    def __calculate_quality(self):
        quality = 0
        quality += self.__calculate_openning_costs()
        quality += self.__calculate_transportation_costs()
        self.quality = quality
        return self.quality

    #DONE
    #Calculates openning costs for the current vector (instance's vector variable) selection
    def __calculate_openning_costs(self):
        cost = 0
        for facility, value in self.vector.items():
            if value['selected'] == True:
                cost += Decoder._openning_costs[facility]
        return cost

    #DONE
    #Calculates the transportation costs for the established routes specified in '_routes' instance variable
    def __calculate_transportation_costs(self):
        cost = 0
        for supplier, route in self._routes.items():
            for demander, products in route.items():
                cost += products*Decoder._transportation_costs[supplier][demander]
        return cost

    #DONE
    #Establishes routes between selected facilities
    def __establish_routes(self):
        #Re-initialize the '_routes' var
        self._routes.clear()
        #Dict struct used to choose the best options to transport products firs
        transportation_costs = dict()
        #Dict struct used to track the product movements in the supply chain
        supply = dict()
        #Dict struct used to track the total amount of products by facility type (or entity)
        total_demands = dict()
        #States the final or end facility type (e.g. 'client')
        final_demander_type = Decoder._supply_direction[-1]
        #'transportation_costs' variable setup
        for supplier, routes in Decoder._transportation_costs.items():
            if self.vector[supplier]['selected']:
                if not supplier in transportation_costs:
                    transportation_costs[supplier] = dict()
                for demander in routes:
                    if self.vector[demander]['selected']:
                        transportation_costs[supplier][demander] = routes[demander]
        #'supply' variable setup
        for facility, amount in Decoder._products.items():
            if self.vector[facility]['selected']:
                if self.vector[facility]['type'] == Decoder._supply_direction[0]:
                    supply[facility] = amount
                else:
                    supply[facility] = 0
        #'total_demands' variable setup
        for entity_type, capacity in self._total_capacities.items():
            if entity_type == Decoder._supply_direction[0]:
                total_demands[entity_type] = capacity
            else:
                total_demands[entity_type] = 0
        #Establish the routes for each type of facility (specified in the '_supply_direction' list)
        for index, supplier_type in enumerate(Decoder._supply_direction[:len(Decoder._supply_direction) - 1]):
            #State the the facility type considered as the demander
            demander_type = Decoder._supply_direction[index + 1]
            #Flag used to check that final (total) demand for the end nodes/facilities is met
            satisfied = False
            #If the total demand for the current demander type is equal to the final demand needed to supply the 'end' nodes or facilities
            if total_demands[demander_type] == self._total_capacities[final_demander_type]:
                satisfied = True
            else:
                #Iterate over the vector to state which is the supplier to consider for supplying its demanders
                for supplier, values in self.vector.items():
                    if values['type'] == supplier_type and values['selected'] and supply[supplier] > 0:
                        #While supplying is still possible for the current supplier facility to its demanders (supplier has available products, available demanders to supply to and the final or end demand hasn't been met)
                        while transportation_costs[supplier] and supply[supplier] > 0 and not satisfied:
                            #Choose the demander (for the currently considered supplier) with the lowest transportation cost
                            demander = min(transportation_costs[supplier].items(), key = lambda item: item[1])[0]
                            #If the demander facility has been selected (in the chromosome/vector) and its demand hasn't been satisfied
                            if self.vector[demander]['selected'] and supply[demander] < Decoder._products[demander]:
                                amount = 0
                                #The amount of products to transport is the remaining amount for the current demander facility to be satisfied
                                if Decoder._products[demander] - supply[demander] <= supply[supplier]:
                                    amount = Decoder._products[demander] - supply[demander]
                                #The amount of products to transport is all the current supplier facility can supply
                                else:
                                    amount = supply[supplier]
                                #The amount of products to transport is the amount that's missing (that the current supplier facility can supply) to satisfy the final (total) demand in the supply chain
                                if total_demands[demander_type] + amount > self._total_capacities[final_demander_type]:
                                    amount = self._total_capacities[final_demander_type] - total_demands[demander_type]
                                #Update the supply dict struct that represents the transportation of products from demand to supplier
                                supply[demander] += amount
                                supply[supplier] -= amount
                                #Update the total amountts of transported products for the considered supplier and demander types
                                total_demands[demander_type] += amount
                                total_demands[supplier_type] -= amount
                                #TEST Error check for verifying capacities are not surpassed
                                if supply[demander] > Decoder._products[demander]:
                                    raise AttributeError("Demander capacity surpassed when supplying {} products from {} to {}. Demander capacity is {} and the supplied amount is {}.".format(amount, supplier, demander, Decoder._products[demander], supply[demander]))
                                #Register transport of products into the '_routes' dictionary
                                if not supplier in self._routes:
                                    self._routes[supplier] = dict()
                                self._routes[supplier][demander] = amount
                            #Remove the already considered demander from the sub-dict struct in the 'transportation_costs' dict struct
                            transportation_costs[supplier].pop(demander)
                            #Check that the final (total) demand has been satisfied for the considered supplier and demander facilities
                            if total_demands[demander_type] == self._total_capacities[final_demander_type]:
                                satisfied = True
                                break #Break while loop
                    #If the final (total) demand is met for the 'end' nodes or facilites, finish the parent 'for' loop
                    if satisfied:
                        break #Break for loop

    #DONE
    #Sort vector based on 'value' of each facility represented in it.
    def __sort_vector(self):
        self.vector = dict(sorted(self.vector.items(), key = lambda entity: entity[1]['value'], reverse = True))
        return self.vector

    #DONE
    #Calculates total capacities per entity type for the selected facilities and stores them on the Decoders instance's private '_total_capacities' dictionary
    def __calculate_total_capacities(self, entity_name = None, add = True):   
        #If the 'self._total_capacities' dict is empty or the 'entity_name' argument wasn't passed, calculate ALL capacities from scratch 
        if not (entity_name):
            self._total_capacities = deepcopy(Decoder._total_capacities_default)
            for key, value in self.vector.items():
                entity_type = value['type']
                if value['selected'] == True:
                    if not entity_type in self._total_capacities:
                        self._total_capacities[entity_type] = Decoder._products[key]
                    else:
                        self._total_capacities[entity_type] += Decoder._products[key]
        #Use the optional arguments to update the '_total_capacities' dict values
        elif entity_name and self._total_capacities:
            entity_type = self.vector[entity_name]['type']
            if add and self.vector[entity_name]['selected'] == True:
                self._total_capacities[entity_type] += Decoder._products[entity_name]
            elif not add and self.vector[entity_name]['selected'] == False:
                self._total_capacities[entity_type] -= Decoder._products[entity_name]
        return self._total_capacities

def main():
    chromosome = [0.51, 0.6, 0.5, 0.2, 0.2, 0.3, 0.52, 0.32, 0.95, 0.85, 0.5, 0.23, 0.143, 0.542]
    test_Decoder = Decoder()
    test_Decoder.load_data()
    print('CHROMOSOME: ', chromosome)
    #DECODE execution TIME
    '''
    start = time()
    end = time()
    print('TIME: ', end - start)
    '''

    test_Decoder.decode(chromosome)

    print('QUALITY: ', test_Decoder.quality)
    print('NEW CHROMOSOME: ', chromosome)

if __name__ == '__main__':
    main()
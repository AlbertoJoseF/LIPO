from random import Random
from collections.abc import Iterable

'''
TODO:

- Check and implement were to type check
    - type checking function

- Document code (Docstrings)
- Include an overall layout (NOT in the Docstrings) of how the function works.

- URGENT: Check were to place the utils functions
    - parameterized_uniform_crossover could be placed in the Individual module as a @staticmethod
        - or could be placed into new class called chromosome (more work)


'''

#Get the highest 'amount' or 'n' values from a list
def get_highest_values(a_list: list, amount: int):
    if not (isinstance(amount, int) or isinstance(amount, float)) or ((amount - round(amount)) != 0) or (amount < 0):
        raise TypeError("Provided 'amount' argument is not a numeric positive whole number. Argument provided is of type: {} and of value: {}.".format(type(amount), amount))
    result = list()
    for item in a_list:
        if len(result) == amount:
            temp = item
            for result_item in result:
                if temp > result_item:
                    temp = result_item
            if temp != item:
                result.remove(temp)
                result.append(item)
        else:
            result.append(item)
    return result

#Get the lowest 'amount' or 'n' values from a list
def get_lowest_values(a_list: list, amount: int):
    if not (isinstance(amount, int) or isinstance(amount, float)) or ((amount - round(amount)) != 0) or (amount < 0):
        raise TypeError("Provided 'amount' argument is not a numeric positive whole number. Argument provided is of type: {} and of value: {}.".format(type(amount), amount))
    result = list()
    for item in a_list:
        if len(result) == amount:
            temp = item
            for result_item in result:
                if temp < result_item:
                    temp = result_item
            if temp != item:
                result.remove(temp)
                result.append(item)
        else:
            result.append(item)
    return result

#Perform parameterized crossover among two list of the same size using a treshold for biasing
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

def main():
    l = ['','','','']
    #print(get_lowest_values(l, 5))
    a_list = parameterized_uniform_crossover([1,2,3,4,5], [6,7,8,9,0], 0.9)
    print(a_list)

if __name__ == '__main__':
    main()
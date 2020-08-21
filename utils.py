from random import Random

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

def main():
    l = ['','','','']
    #print(get_lowest_values(l, 5))
    a_list = parameterized_uniform_crossover([1,2,3,4,5], [6,7,8,9,0], 0.9)
    print(a_list)

if __name__ == '__main__':
    main()
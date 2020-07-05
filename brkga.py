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
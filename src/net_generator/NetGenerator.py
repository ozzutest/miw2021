
import random

class NetGenerator:

    """
        The structure for neural net generator.
    """

    def __init__(self):
        self.structure = []
        self.values = []
        self.interval = []


    # Function generates random values based on user input
    def generate_random_values(self):
        
        counter = 0
        for i in range(1, len(self.structure)):
            # append bias and other nodes
            counter += self.structure[i - 1] * self.structure[i] + self.structure[i]
        
        try:
            _min = self.interval[0]
            _max = self.interval[1]
        except IndexError: print("Could not read the min, max values")
    
        # generate from default values
        if not self.structure: 
            print("First, set the structure.")
            return

        for node in range(counter):
            if _min == 0 and _max == 1:
                # append the float numbers based on interval 0 from 1.
                self.values.append(random.random())
            else:
                # otherwise append the random values based on min and max input
                self.values.append(random.uniform(_min, _max))

        # if all possibilites are generated...
        return self.__save_the_structure()

    # Function saves the data structure
    def __save_the_structure(self):

        if self.interval and self.values and self.structure:
            return [self.structure, (self.interval[0], self.interval[1]), self.values]




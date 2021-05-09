
import sys
import json
import os
from NetGenerator import NetGenerator


class NetLoader:

    """ The menu for net generating 
        In the menu, user can pick the shape of structure - pressing 1.
        User also can define the numerical interval for generting values - pressing key 2.
        User has possibility to the quity program pressing key 3.
    """
    structure = []

    def __init__(self):
        self.welcome_user()
        # initialize the NetGenerator object
        self.netgenerator = NetGenerator()
        # assign here the net instance
        self.choices = {
                '1': self.generate_structure,
                '2': self.set_values,
                '3': self.save_file,
                '4': self.read_file,
                '5': self.quit_program
        }

    
    def welcome_user(self):
        """ Initial information on startup. """
        print(
                """
                Hello User! This program generates the values for neural network.
                The instructions are described below:
                The available options are numbers (1. - 3.)
                1. Sets the specification of the given structe in the following input:
                For example: 3-2-2 or 3 2 2, where:
                    - first value defines the nodes in first layer,
                    - second value defines the nodes in 2nd layer,
                    - third value defines the nodes in 3rd layer.
                2. Sets the value interval for generating the values based on amount of edges.
                3. Saves the generated values to a file. In saving method type the exisiting dircetory to save a file.
                    For example: C:\\Users\\<username>\\<folder_to_save_the_file>
                4. Load the data. 
                5. Quit the program
                """)

    def display_menu(self):
        """ The avaliable options to pick from the menu. """
        print("""
            1. Set the structure (Example of valid input: 3-2-2 or 3 2 2).
            2. Set the interval of generating values. (Default is 0 - 1).
            3. Save the generated values to a file.
            4. Load the data.
            5. Terminate the program.
            """)

    def run(self):
        """ The function runs the program and prints the output for specific option """
        while True:
            self.display_menu()
            choice = input("Choice: ").strip()
            self.temp = choice
            result = ''
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f'The choice {choice} is invalid.')
 
            print() 
            result += self.__summary_information()
            print(result)

    def quit_program(self):
        """ Function terminates the program """
        print('Program has been terminated.')
        sys.exit(0)


    def generate_structure(self):
        """ The function is responsible for validating the user input and saves the information about the structure """
 
        structure_params = input("Type the structure (separated with '-' or ' '): ")
        
        is_valid = self.validate_the_input(structure_params)
       
        if not is_valid: return
        
        if '-' in structure_params:
            structure_params = structure_params.rstrip().split('-')
        else:
            structure_params = structure_params.rstrip().split(' ')

        print(f'\n[INFO] The edges, values and nodes will be generated for structure: {structure_params}')
       
       # end here
       # assign the structure params for generator object

        try:
            structure_params = [int(param) for param in structure_params]
        except Exception as e:
            print(e)
        
        # assign the structure params to the object
        self.netgenerator.structure = structure_params
        
    def set_values(self):
        """ The function sets the divison value for generting the weights. """

        value_interval = input("Type the value interval to generate the weights (Example: -1 2): ") 

        print("\n[ATTENTION] The default value interval: [0, 1].")
        
        if not value_interval: value_interval = '0 1'

        if_valid = self.validate_the_input(value_interval)

        if not if_valid: return
        
        if ' ' in value_interval: value_interval = value_interval.rstrip().split(' ')
        elif '-' in value_interval: value_interval = value_interval.split('-')

        parsed = [int(value) for value in value_interval]

        if parsed[0] > parsed[-1]: 
            _max, _min = parsed[0], parsed[-1]
        elif parsed[-1] > parsed[0]: 
            _max, _min = parsed[-1], parsed[0]
        else: 
            _min, _max = parsed[0], parsed[-1]

        print(f"\n[INFO] Generating the values from range: {_min, _max}.")
        self.netgenerator.interval = [_min, _max]
        self.structure = self.netgenerator.generate_random_values()
        
    def validate_the_input(self, _input):
        
        if not any([value.lstrip('-+').isdigit() for value in _input]):
            print("\n [ERROR] The value should be the numeric.")
            return False

        if ' ' in _input:
            # cut the white space from the end of input
            input_values = _input.rstrip().split(' ')
        elif '-' in _input: 
            input_values = _input.rstrip().split('-')
        else:
            input_values = ''

        # check the input based on the option from menu 
        if self.temp == '1':

            if len(input_values) < 3: 
                print("\n [ERROR] Minimum required length of generating structure should be the 3.")
                return False
            
            if not all([value.isdigit() for value in input_values]):
                print('\n [ERROR] The input is invalid.')
                return False

        if self.temp == '2':
            
            if len(input_values) != 2:
                print('\n [ERROR] The length of input value is invalid. The proper length is 2.')
                return False

            if not all([value.lstrip('-+').isdigit() for value in input_values]):
                print('\n [ERROR] The input is not of numeric type.')
                return False
        
        return True


    def __summary_information(self):
        print("\n\n [INFO] Your inputs: ")
        output_string = ''
        if self.netgenerator.structure:
            output_string += f'\tstructure: {self.netgenerator.structure}' + '\n'
        if self.netgenerator.interval:
            output_string += f'\tmax, min: ({self.netgenerator.interval[0]}), ({self.netgenerator.interval[1]})' + '\n'
        if self.netgenerator.values:
            output_string += f'\tgenerated values: {self.netgenerator.values}' + '\n'
        
        return output_string

    def save_file(self):
        """ Function saves the generated weights based on structure to the file. """

        import string, re
        punctuations = list(str(_str) for _str in string.punctuation)
        _string = '' 
        for _str in punctuations: _string += _str

        output_directory = input("Specify the path to save the structure data: ")
        if not os.path.exists(output_directory): 
            print("\n [ERROR] The given folder does not exist.")
            answer = input("Create folder? (yes/no): ")
            if answer.lower() == 'yes':
                
                print("\n [INFO] Folder will be created in current directory.")
                print("\n [INFO] Specify the name of the folder without special characters.")

                name_of_folder = input("Name of the folder: ")
                extract = re.split('[' + _string + ']', name_of_folder)
                filtered = list(filter(lambda x: x, extract))

                try:
                    name_of_folder = filtered[0]
                except IndexError as e: print(e)
                    
                # specify the name of folder
                
                parent_dir = os.getcwd()
                path = os.path.join(parent_dir, name_of_folder)
                os.mkdir(path)
                print(f'\n [INFO] Path {path} created succesfully.')
                
                # set the output to the actual created path
                output_directory = path

            elif answer.lower() == 'no':
                print(f'\n[ERROR] Try again.')
                return 

            else: 
                print('[ERROR] Wrong answer.')
                return
        
        
        filename = input("\nSpecify the filename of the file. (The file is in json format): ")
        if not filename: 
            print(f'\n[ERROR] Empty input.')
            return

        # split the output based on special chars
        extracted = re.split('[' + _string + ']', filename)
        # filter if the string is empty
        filtered = list(filter(lambda x: x, extracted))
        # always pick the first position
        try: 
            filename = filtered[0]
        except IndexError as e: print(e)
        format_file = '.json'
        if not self.structure: 
            print("\n [ERROR] The structure is not ready yet to save to the file. Fullfill the other needed fields.")
            return

        data = {}
        try:
            data['structure'] = self.structure[0]
            data['interval'] = { 'min': self.structure[1][0], 'max': self.structure[1][1] }
            data['values'] = self.structure[-1]
        except IndexError: print('Index error.')
        
        abs_path = os.path.abspath(output_directory)
        dest = os.path.join(abs_path, filename + format_file)

        if not os.path.exists(abs_path): 
            print("\n [ERROR] Given path does not exists.")
            return

        with open(dest, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
        print(f"\n [INFO] Succesfully saved file {filename}{format_file} to {abs_path}.")
        return 

    def read_file(self):
 
        """ Function reads the structure from json file """
        from glob import glob
 
        result = [y for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.json'))]

        if not result: print(f"\n[INFO] The file is not found in current directory.")
        
        print(f'Possible files: ')
        for value in result:
            print(value)

        file_directory = input("\nPath to file  (absolute): ")

        if not os.path.exists(file_directory):
            print("\n [ERROR] Given path does not exist.")
            return

        abs_path = os.path.abspath(file_directory)
        result = [y for x in os.walk(abs_path) for y in glob(os.path.join(x[0], '*.json'))]

        print(f"\n[INFO] Founded json files in directory: ")
        for value in result:
            print(value)
    
        if not result:
            print(f"\n [ERROR] json file does not exist in directory {abs_path}.")
            return 

        info = {}
        for index, value in enumerate(result):
            base = os.path.basename(value)
            filename, ext = os.path.splitext(base)
            info[index] = [base, filename, ext]

        load_file = input("\nThe filename of file to read (possible with extension): ")

        file_to_read = ''
        for key, value in info.items():
            for inner_value in value:
                if inner_value == load_file:
                    file_to_read = inner_value
                    break

        if not file_to_read:
            print(f"\n[ERROR] The file {load_file} does not exist. ")
            return
    
        if not '.' in file_to_read:
            file_to_read += '.json'

        
        with open(file_to_read) as f:
            data = json.load(f)

<<<<<<< HEAD

        __ALLOWED = ['structure', 'interval', 'values']
        args = []

        for key, item in data.items():

            if key not in __ALLOWED:
                print(f"\n [ERROR] Wrong key! Proper keys: {__ALLOWED}")
                break

            if not (isinstance(item, list)) and not (isinstance(item, dict)): 
                print(f'\n [ERROR] All key values should be a type as dictionary or list.')
                return
        
            if isinstance(item, dict):
                test_max, test_min = item.get('max'), item.get('min')
               
                if not (isinstance(test_min, int)) and not (isinstance(test_max, int)):
                    print("\n [ERROR] The min, max value should be an integer.")
                    return

            if isinstance(item, list):

                for element_type in item:
                    if not (isinstance(element_type, int)) and not (isinstance(element_type, float)):
                        print(f'\n [ERROR] The elements in list should be numeric!')
                        return
            
=======
        print(f"\n [INFO] Successfully read the json file.")
        args = []
        for key, item in data.items():
            print(f'{key}: {item}')
>>>>>>> 2c06d3924724775ba8a87e4e284ef15b7a61e7ff
            args.append(item)

        if len(args) == 3:
            try:
                self.netgenerator.structure = args[0]
                interval = args[1]
<<<<<<< HEAD
                _min, _max = interval.values()
                self.netgenerator.interval = _min, _max
                self.netgenerator.values = args[-1]
            except IndexError as e: print(e)

        return data

         
=======
                _min, _max = interval.items()
                self.netgenerator.interval = [_min, _max]
                self.netgenerator.values = args[-1]
            except IndexError as e:
                print(e)

        return data         
>>>>>>> 2c06d3924724775ba8a87e4e284ef15b7a61e7ff


if __name__ == '__main__':
    NetLoader().run()




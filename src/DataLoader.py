
import json
import os


class DataLoader:
    """ 
    The data loader config, initializes the dataset from .json config file.
    Data loader splits the file into particular fields:
    filename - the filename of dataset
    decision_class - the chosen index column of decision class in dataset,
    input_cols - the inputs of data set,
    row_range - the range of rows from start index to stop index,
    normalize_data - the function to normalize data (if false, the data stays unormalized),
    sym_to_num - function to change symbolic data to numeric,
    save_to_dir - saves the dataset to given directory.
    """

    def __init__(self, path_to_config):
        if os.path.isfile(path_to_config):
            self.path_to_config = path_to_config
        else:
            raise FileNotFoundError(f'The file at path {path_to_config} does not exist! Create config.json file!')


    def initialize(self):
        return self._check_file()

    def _check_file(self):
        base = os.path.basename(self.path_to_config) # extracts the filename config with .json extension
        filename, ext = os.path.splitext(base) # splits the file to filename and extension
        
        # checks the file extension
        if ext != '.json': raise ValueError(f'The file {filename} of extension {ext} is the wrong type! (Extension .json is correct).')

        # checks the content of .json config
        if os.path.getsize(self.path_to_config) <= 0: raise OSError('The file is empty!')

        with open(self.path_to_config) as _file:
            config_data = json.load(_file)
        
        proper_keys = ['filename', 'decision_class',  'delete_column', 'input_col', 'row_range', 'normalize_data', 'normalize_column',  'describe_column', 'sym_to_num', 'save_to_dir', 'file_extension', 'delimiter']
        
        # check  if column_description in config
        if "column_description" in config_data.keys():
            proper_keys.append("column_description")

        # check if the number of keys in config file and in proper list is equal
        if len(config_data.keys()) != len(proper_keys):
            print('The list of proper keys: ')
            print([x for x in proper_keys])
            raise ValueError(f'The number of keys is not equal!')

        for key in config_data.keys(): # checks if key is proper in config file 
            if key not in proper_keys: raise KeyError(f'The {key} is not proper key in config keys!')
       
        # extract the key values
        key_values = []
        for key in config_data.keys():
            value = config_data.get(key)
            if value == None: raise ValueError(f'The value {value} of {key} is empty!')
            key_values.append(value)


        # check if data file exists and is proper
        (filename, decision_class, delete_column, 
        input_col, row_range, normalize, col_normalize, 
        describe_column, sym_to_num, directory, 
        file_ext, delimiter) = (key_values[0], key_values[1], key_values[2], 
                                key_values[3], key_values[4], key_values[5],
                                key_values[6], key_values[7], key_values[8], 
                                key_values[9], key_values[10], key_values[11])

        # returns the all validated fields like filename, decision_class, etc...
        if (self._check_data_file(filename) and self._check_decision_class(decision_class)
                and self._check_input_cols(input_col) and self._check_row_range(row_range)
                and self._check_normalize(normalize) and self._check_sym_to_num(sym_to_num) 
                and self._check_save_to_dir(directory) and self._check_file_extensions(file_ext)
                and self._check_delimiter(delimiter) and self._check_delete_columns(delete_column) 
                and self._check_column_to_norm(col_normalize) and self._check_describe_column(describe_column)):

               return filename, decision_class, delete_column, input_col, row_range, normalize, col_normalize, describe_column, sym_to_num, directory, file_ext.lower(), delimiter
        
        #if the file is ok, just return the tuple of values from config 
        
    # checks the data file, if exists and have proper extension        
    def _check_data_file(self, filename):
        if not os.path.isfile(filename): raise FileNotFoundError(f'The dataset file {filename} does not exist!')
        
        extensions = ['.csv', '.txt', '.dat', '.data', '.xlsx', '.json']
        
        base = os.path.basename(filename)  
        filename, ext = os.path.splitext(base) # check if dataset has the proper format

        if any([_ext for _ext in extensions if _ext == ext.lower()]): return True

        raise ValueError(f'The inappropriate file extension - {filename}{ext}. The correct extenions of dataset file are: (.csv, .txt, .dat, .data, .xlsx, .json)')
    
    # check if the decision class is the right type
    def _check_decision_class(self, decision_class):

        if not isinstance(decision_class, list): raise ValueError('The value of decision class key is not a list (it should point the column index in []!)!')
        
        if not decision_class: raise ValueError('The list of decision class field is empty!')

        return True

    # checks if input columns are list
    def _check_input_cols(self, input_col):
        
        if not isinstance(input_col, list): raise ValueError('The input columns (indexes) are not in list!')

        if not input_col: raise ValueError('The list of input columns field is empty!')

        return True

    # checks if the row range is list
    def _check_row_range(self, row_range):

        if not isinstance(row_range, list): raise ValueError('The row range are not put in list! Proper way: [index_start, index_stop]!')

        if not row_range: raise ValueError('The list of row range field is empty!')

        return True

    # checks if the normalize data is boolean

    def _check_normalize(self, to_normalize):

        if not isinstance(to_normalize, bool): raise ValueError('The value of key normalize_data is not boolean! (True/False only)!')

        return True


    # checks if sym_to_num is bool
    def _check_sym_to_num(self, sym_to_num):

        if not isinstance(sym_to_num, bool): raise ValueError('The value of key sym_to_num is not boolean! (True/False) only!')

        return True 

    # checks if the directory exists and if directory is type of string
    def _check_save_to_dir(self, directory):

        if not isinstance(directory, str): raise ValueError('The value of dir key is not a string!')

        if not os.path.isdir(directory): raise FileNotFoundError('Given directory does not exist! Choose existing directory to save file.')

        return True


    def _check_file_extensions(self, file_ext):

        if not isinstance(file_ext, str): raise TypeError('The value of key file extension is not string!')

        allowed_ext = ['csv', 'txt', 'json']
        
        if file_ext.lower() not in allowed_ext: raise ValueError(f'Inappropriate file extension in value of key file extension!\nAllowed extensions to save the file are: {allowed_ext}')

        return True


    def _check_delimiter(self, delimiter):
        
        if not isinstance(delimiter, str): raise TypeError('The delimiter value is not a string!')

        if not delimiter: raise ValueError('The delimiter value string is empty!')

        allowed_delimiters = [';', ',', ' ', '_', '#', '|']

        if delimiter not in allowed_delimiters: raise ValueError(f'The delimiter is wrong! Allowed delimiters: {allowed_delimiters}')

        return True

    def _check_delete_columns(self, delete_param):

        if not isinstance(delete_param, list): raise TypeError('The value of key "delete_column" is not a list!')

        if delete_param:
            for value in delete_param:
                if not isinstance(value, int): raise TypeError('The index in list is not an integer.')


        return True

    def _check_column_to_norm(self, column_to_norm):

        if not isinstance(column_to_norm, list): raise TypeError('The value of key "normalize_column" is not a list.')
        
        if column_to_norm:
            for value in column_to_norm:
                if not isinstance(value, int): raise TypeError('The index of column to normalize is not an int.')

        return True

    def _check_describe_column(self, describe_column):
        
        if not isinstance(describe_column, list): raise TypeError('The "describe_column" value is not a list.')

        return True



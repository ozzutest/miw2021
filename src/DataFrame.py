
import os
import re
import copy
import csv
import sys
import json
from datetime import datetime
from DataLoader import DataLoader
from collections import ChainMap, Counter


class DataFrame:
    """
    The dataframe to keep the data from dataset. 
    The datastructure is the list of lists, each row (list) is exactly the same as data set from file.
    
    """

    df = []
    inputs = []
    decision_class = []
    primal_decision = []

    def __init__(self):
        # path to config file
        self.filename, self.config_args = self._unpack_data() 
        
        # load the data to data frame structure
        for line in open(self.filename, 'r'):
            self.df.append([line.strip()])

        self._split_datapoints()
        self._delete_columns()
        self._set_row_range()
        self._clean_data()
        column_description = self._describe_column()
        if column_description:
            self._save_description_to_config(column_description) 
        # add here function to save the column params
        self._parse_datapoints()
        

        # MAKE here validation to check if sym_to_num or other fields are TRUE from config file
        try:
            bool_normalize = self.config_args[4]
            bool_sym_to_num = self.config_args[7]
        except IndexError:
            print('Index out of range!')
        finally:
            if bool_sym_to_num:
                # TODO: return here the infomartions about the converted symbolic columns
                self._sym_to_num()
            if bool_normalize:
                self._normalize_datapoints()
        self.inputs = self._take_columns(self.config_args[2])
        self.decision_class = self._take_columns(self.config_args[0])
        # TODO: end up _num_to_sum
        #if num_to_sum_info:
        #    self.primal_decision = self._num_to_sum(num_to_sum_info)
        self._save_dataset()

    def _unpack_data(self):
        # load the DataLoader object 
        dl = DataLoader(os.getcwd() + r'\config.json') 
        
        # unpack the data from object
        filename, *config_args = dl.initialize()

        return filename, config_args


    def _split_datapoints(self):
        # split the datapoints by ,;: or space
        self.df = [re.split(r'[,;:]| ', x) for line in self.df for x in line]

        return self 
    
    # function deletes columns based on the index from config file
    def _delete_columns(self):
        
        # try get the parameter from config 
        try:
            columns_list = self.config_args[1]
        except IndexError:
            print('List of column indexes does not exist.')
        
        # if list of indexes in column is empty, nothing to do nor delete
        if not columns_list:
            return

        rows = copy.deepcopy(self.df)
        columns = list(zip(*rows))  
        # foreach column index in self.df
        for column_index in range(len(columns)):
            # foreach column index from config file
            for index_column in columns_list:
                # if column index from df is equal to column index from file
                if column_index == index_column:
                    # pop the column
                    columns.pop(column_index)


        transposed = list(map(list, zip(*columns)))
        self.df = transposed[:]

        return self


    # convert from string to numeric
    def _parse_datapoints(self):
        # check whether str element is int or float
        validate_point = re.compile(r'(\d+(?:\.\d+)?)')  
        # rows from self.df
        rows = copy.deepcopy(self.df)
        # create columns from rows
        columns = list(zip(*rows))
        # indexing the columns
        for column in range(len(columns)):   
            # make the tuple column a list to be able to parse elements at index position
            tmp = list(columns[column])            
            for element in tmp:
                # take index of every element
                index = tmp.index(element)                 
                # swap str element to float if numeric
                if validate_point.match(element): tmp[index] = float(element)

            columns[column] = tuple(tmp)
        
        # transpose the columns again to rows
        transposed = list(map(list, zip(*columns)))  
        self.df = transposed[:]

        return self
        



    # cleans data from values NULL, NaN, '', etc.
    def _clean_data(self):
        pattern_to_remove = ['?', 'NULL', '', 'NaN', 'nan', ' ', None, 'null']
        # take indexes if values are empty
        rows = copy.deepcopy(self.df) # make rows from dataframe 
        columns = list(zip(*rows)) # rows to columns
        indexes = []

        for column in range(len(columns)):
            # foreach column tuple to list
            tmp = list(columns[column])         
            # for index and value of lists elements
            for index, value in enumerate(tmp):                 
                # if value is like ?, NULL,  NaN, add to list of indexes its position
                if value.lower().strip() in pattern_to_remove: indexes.append(index)    

        # for index in indexes list, remove the ones with containg the null values
        for index in sorted(set(indexes), reverse=True): 
            if 0 <= index < len(self.df): self.df.remove(rows[index]) 


        return self


    # prints the input columns in human format
    def print_inputs(self):
        # pretty print the 2D array
        return  '\n'.join(['\t\a\a\a\a'.join(["%0.4f" % cell for cell in row]) for row in self.inputs])
 
    
    # prints in human format the decision class
    def print_decision_class(self):
        return '\n'.join(['\t\a\a\a\a'.join(["%0.4f" % cell for cell in row]) for row in self.decision_class])

    def print_primal_decision_class(self):
            return '\n'.join(['\t\a\a\a\a'.join(["%s" % cell for cell in row]) for row in self.primal_decision])

    # prints the data structure in human format
    def __str__(self):
        return '\n'.join(['\t\a\a\a\a'.join(["%0.4f" % cell for cell in row]) for row in self.df])


    # prints the shape _of dataset (n rows x n cols)
    def get_shape(self):

        n_rows = len(self.df)
        n_cols = len(self.df[0]) if self.df else 0

        return n_rows, n_cols

    # creates the dictionary with string values and convert them to numeric
    def _sym_to_num(self):
        
        # create columns from dataframe
        columns = list(zip(*self.df))
        # pick the columns contain str data points
        str_columns = [[value for value in column if isinstance(value, str)] for column in columns]
        # filter the values of data points 
        filtered = [dict([(index, sorted(set(col)))]) for index, col in enumerate(str_columns) if col] 
        # create dictionary with index and value of given column
        hash_table = dict(ChainMap(*filtered)) 
        if not hash_table: 
            print('All columns in dataset are numeric, no need to convert datapoints.')
            return

        # sort the dicitonary by column index in ascending order
        keys = sorted(hash_table)
        _sorted = { k: hash_table[k] for k in keys }
    
        # creating the dictionary with keys as values from datasets and values as numeric value
        columns = list(_sorted.keys())

        # take string values for columns
        values = [value for value in _sorted.values()]

        # for each value in column assign the number value by index of this string value
        unpacked = [{ k: v for k, v in zip(value, range(len(value))) } for value in values]

        # merge column index and values
        merged = {k: v for k, v in zip(columns, unpacked)}
        
        # print information about permutation
        for column, values in merged.items():
            print(f'Column: {column}')
            for k, v in values.items():
                print(f'\titems: {k} -> {v}')
          
        # reverse the process from symbolic to numeric

        # TODO: repair the primal symbolic values from numeric, return the "new" variable
        """
        _reversed = [merged.get(column_index) for column_index in self.config_args[0]]
        print(f"reversed: {_reversed}")
        #new = []

        # get index of column and numeric to symbolic values
        if all(_reversed):
            new = [(value, {k: v for k, v in zip(_dict.values(), _dict.keys())}) for value, _dict in zip(merged.keys(), _reversed)]           
            print(f'new: {new}')
        """
        dicts = [merged.get(column) for column in merged.keys()]
        # again operating at rows from self.df
        rows = [row[:] for row in self.df]
        
        # create columns
        df_columns = list(zip(*rows))
                  
        # foreach column index from dataframe
        for df_col_ind in range(len(df_columns)):
            # temporary variable to get list of values from columns
            tmp = list(df_columns[df_col_ind])
            # foreach column index which its values are string
            for mer_col_ind in merged.keys():
                # if index of column of string values from dataframe is the same as the grabbed string columns from dataset
                if df_col_ind == mer_col_ind:
                    # unpack dictionary containing key: values (string values and numeric values)
                    values = merged.get(df_col_ind)
                    # unpack keys (string) values
                    keys = list(values.keys()) 
                    # unpack the numeric values 
                    numeric_values = list(values.values())
                    # foreach value and key in keys and numeric values
                    for key, value in zip(keys, numeric_values):
                        # foreach element in dataframe column
                        for df_value in range(len(tmp)):
                            # if key is the same as the value from dataframe
                            if key == tmp[df_value]:
                                # swap to numeric value
                                tmp[df_value] = value
        
            # again convert column to tuple to transpose column into rows 
            df_columns[df_col_ind] = tuple(tmp)


        transposed = list(map(list, zip(*df_columns)))
        self.df = transposed[:]
        return self

    # TODO: swap the indexes after the deletion of column
    # function that takes the parsed data points and turns them to original symbolic values
    def _num_to_sum(self, information):
        
        if not information: 
            print("Nothing to change. All values of decision class are primal numeric.")
            return
    
        # grab column indices
        column_indices = [_tuple[0] for _tuple in information]     
        transposed = list(map(list, zip(*self.df)))
        for col_ind, _col_ind in zip(column_indices, range(len(transposed))):
            if col_ind != _col_ind:
                continue
            
            # take the values to swap
            swap_values = [_tuple[1] for _tuple in information]

            # foreach value in transposed
            for value in transposed[col_ind]:
                # for dictionary with values sym to num
                for s_value in swap_values:
                    # append to primal decision the values from num to sym
                    self.primal_decision.append([s_value.get(value)]) 

        #self.primal_decision = list(zip(*self.primal_decision)) 
        return self.primal_decision
       
    # normalizes the data to range (0 - 1)
    def _normalize_datapoints(self):
        # get rows from dataframe 
        rows = [row[:] for row in self.df]
        # make columns
        columns = list(zip(*rows))

        if any([isinstance(value, str) for column in columns for value in column]): raise ValueError('The dataset contains string values! Convert symbolic values to numeric first.')
        
        try: 
            decision_class = self.config_args[0]
        except IndexError: print(f'The given index of decision class from config does not exist in dataframe!')
       
        try: 
            columns_to_normalize = self.config_args[5]
        except IndexError: print(f'The given index of column to normalize does not exist')

        # get list of normalized data as columns
        normalized = []

        # validate if decision class is to be normalized and check the index of columns to norm
        for value in columns_to_normalize:
            if value in decision_class:
                raise ValueError("Decision class column can not be normalized.")
            if value not in range(len(columns)):
                raise ValueError(f"{value} is not the existing index of data frame.")

        # grab the data to normalize
        columns_index = [col_ind for col_ind in range(len(columns)) if col_ind in columns_to_normalize]

        # foreach column do
        for index in columns_index:    
            # make the temporary list of column
            for dec_index in decision_class:
                if dec_index == index:
                    continue
                temporary = list(columns[index])
                # take max and min value from column
                _min, _max = min(temporary), max(temporary)
                # foreach element in column subtract the min value and divide by max value + min value
                # append the result to normalized list as tuple (column) 
                if _min == _max: # prevent dividing by zero
                    continue
                normalized.append(tuple([(x - _min) / (_max - _min) for x in temporary]))

        # foreach column in columns, pop the normalized column and assign to the proper index
        for index in columns_index:
           columns[index] = normalized.pop(0)

        # tranpose columns to rows
        transposed = list(map(list, zip(*columns)))
        self.df = transposed[:]

        return self


    # takes the inputs columns
    def _take_columns(self, conf_args):
        # try take the index of inputs columns from config file
        try:
            conf_columns = conf_args
        except IndexError:
            print(f'IndexError, index {columns_from_config} of column does not exist in dataframe!')
            return
    
        # take rows from dataframe 
        rows = [row[:] for row in self.df]

        # transpose rows to columns
        columns = list(zip(*rows))
        # take index of columns from dataframe
        index_columns = list(range(len(columns)))


        # intersection of two sets - the norm_row_rangeinput columns and columns from dataset
        common_index = set(index_columns) & set(conf_columns)

        # check if any index from config file does not belong to the index of columns from dataframe
        if not common_index: raise IndexError(f'The index of input columns from config file is wrong!\nThe proper index of columns: {[str(x) for x in index_columns]}')
        
        
        # iterate for every element from dataframe column by ith index from intesection set
        filtered = [tuple([element for element in columns[index]]) for index in common_index]
        
        # assign the inputs
        transpose = list(map(list, zip(*filtered)))
        columns = copy.deepcopy(transpose)
        
        return columns


    # function sets the row range in dataframe (index_start, index_stop)
    def _set_row_range(self):
        
        # set row range
        try: 
            row_range = self.config_args[3]
        except IndexError:
            print('Could not read the index from row range field!')
            return
        
        # if the length of list of indexes from config > 2, return ValueError
        if not len(row_range) <= 2: raise ValueError('The list of indexes are too long! (Required values: index_start, index_stop)')

        n_rows, cols = self.get_shape()
        rows = self.df[:]
        
        # check if value is not 'full', othwerise cut the list from index_start, index_stop
        if 'full' not in row_range:
            # unpack values from config
            index_start, index_stop = row_range[0], row_range[1]
            # validate the indexes
            if 0 <= index_start < index_stop and index_start < index_stop <= n_rows:
                # cut the list from index_start to index_stop (index_stop is always index_stop := -1)
                self.df = rows[index_start: index_stop]
            else:
                raise IndexError(f'The index is out of range! The number of rows: {n_rows}!\n (0 <= index_start < index_stop)')
        else:
            pass

        return self

    # function saves the dataframe to destination path from config file with suitable extension
    def _save_dataset(self):
        # unpack the values from config file
        try:
            basename = os.path.basename(self.filename)
            base_file, ext = os.path.splitext(basename)
            file_extension = self.config_args[9]
            destination_path = self.config_args[8]
            delimiter = self.config_args[10]
        except IndexError:
            print('Index is out of range! Could not take the file extension and destination path!')
            return
        
        # HERE TODO: ensure if save to file only decision class with normalized inputs or save the whole dataset
        # saved dataset are modified

        now = datetime.now()
        filename = f'{now.strftime("%H_%M_%S")}_dataset_{base_file}'
        path_to_save = os.path.join(destination_path, filename + '.' + file_extension)
        data_to_save = []
        inputs = self.inputs
        decision_class = self.decision_class
        if not inputs and decision_class:
            raise ValueError("Input columns or decision class is not defined!")

        if decision_class and inputs:
            parsed = [[row[col] for row in inputs] for col in range(len(inputs[0]))]
            floaten = [value for inner in decision_class for value in inner]
            parsed.append(floaten)
            rows = [row for row in parsed]
            columns = list(zip(*rows))
            
        if file_extension != 'json':
            # if file_ext is not json write file as csv or txt
            with open(path_to_save, 'w', newline='\n') as _file:
                csv.writer(_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL).writerows(columns)
        else:
            # otherwise save as json file
            with open(path_to_save, 'w') as _file:
                    _file.write(json.dumps([[str(x) for x in lst] for lst in columns], indent=4))

        print(f'[{datetime.now()}] Succesfully saved the dataset at: {path_to_save}.')

        return
            
    # desrcibes the column info from config file
    def _describe_column(self):
        
        # take rows from dataframe
        rows = [row for row in self.df]
    
        # take index of columns 
        columns = list(zip(*rows))

        # take columns index to check if the index of column exists
        columns_index = list(range(len(columns)))
    
        # check if column index exists in data frame
        try:
            config_columns_index = self.config_args[6]
        except IndexError:
            print('Given column index does not exist.')
        
        if "full" in config_columns_index:
            config_columns_index = [index for index in range(len(columns_index))]

        # check if the column index to describe exists in dataframe
        for index in config_columns_index:
            if index not in columns_index: raise ValueError(f'The given index {index} of column does not exist in data frame.')

        parameters = []

        # get column data from data frame
        if config_columns_index:
            for column_index in config_columns_index:
                data = columns[column_index] 
                # extract from column info important data 
                # check if value in column is an integer either string
                for value in data[:1]:
                    # check if value is string
                    if isinstance(value, str):
                        # if value is a numeric value 
                        if value.replace('.', '', 1).isdigit():
                            # convert data to float
                            data = [float(value) for value in data]
                            # take min value, max value and the average from collection
                            min_value = min(data)
                            max_value = max(data)
                            # take most_common element
                            most_common = Counter(data).most_common(1)[0]
                            # decide if use arithmetic average or mean average...
                            if len(data) != 0:
                                avg = sum([value for value in data]) / len(data)
                            # append parameters to the list
                            parameters.append((column_index, min_value, max_value, most_common, avg))
                        else:
                            # if value is a string take the most common occurences and least
                            most_common = Counter(data).most_common()[0]
                            least_common = Counter(data).most_common()[-1]
                            parameters.append((column_index, [most_common], [least_common]))

        # flat the Counter object
        from collections import defaultdict
        output = defaultdict(list)
        # check if parameter in list is either float or string
        for element in parameters:
            # take the column index
            column_index = element[0]
            # recognize if the column has the float elements
            # append to dictionary the informations about columns
            if isinstance(element[1], float):
                keys = ['column_index', 'min_value', 'max_value', 'most_common_value', 'average']
                # append to the dictionary keys and values
                output[column_index].append({ key : value for key, value in zip(keys, element) })
            # or strings
            elif isinstance(element[-1], list):
                keys = ['column_index', 'most_common_value', 'least_common_value']
                output[column_index].append({ key : value for key, value in zip(keys, element) })

            
        return output
    
    # function saves the column description based on provided column index from json file
    def _save_description_to_config(self, description_of_column):
       # json to load
        if not isinstance(description_of_column, dict): raise TypeError("The description of column should be a dicitonary.")
        _file = os.getcwd() + r'\config.json'

        output_file = {}
        if os.path.isfile(_file):
            # check if the key in config file exists already
            with open(_file, 'r') as file_read:
                keys_from_file = json.load(file_read)
            
            # check if the column description exists in config file
            for key in keys_from_file.keys():
                if key == "column_description" in key:
                    print("Only one column has to be described. Delete exisitng key 'column_description'.")             
                    return
            
            # if it does not, write to the file specific description of column
            with open(_file, 'r+') as f:
                # find the end of the file
                f.seek(0, 2)
                # search the position to append the content
                position = f.tell() - 2
                f.seek(position)
                f.write(',\n')
                # write to the file
                f.write('\t"column_description":')
                f.write(f" {json.dumps(description_of_column, indent=8, sort_keys=True, ensure_ascii=False)}")                
                f.write("}") 




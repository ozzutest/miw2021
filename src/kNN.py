

import math
import copy
from operator import itemgetter
from collections import Counter, defaultdict

class kNearestNeighbors:

    """ 
        The k - Nearest Neighbor machine learning classificator.
        The supervised algorithm for classification.
        Available metrics are with provided examples of attributes:
            - Euclidean - 'euclidean',
            - Minkowski - 'minkowski',
            - Manhattan - 'manhattan'.
        Constructor parameters:
            - k - defnies the number of the nearest neighbors (example: k = 3),
            - distance - defines the metric to use (example: distance = 'minkowski').
        The implementation of this algorithm is based on 1st variation
        (The amount of k neighbors decides about the decision class).
    """

    __METRICS = ['euclidean', 'manhattan', 'minkowski']

    def __init__(self, k=3, metric='euclidean'):
        """ 
            The constructor for algorithm
        """
        self.__fit_data = []
        if not isinstance(k, int): raise TypeError("Wrong type of k parameter")
        if k < 0: raise ValueError("The 'k' paramter should be greater than 0.")
        if metric.lower() not in self.__METRICS: raise ValueError("Inaproperiate metric value.")
        self.k = int(k)
        self.metric = metric

    # Euclidean metric function
    def __euclidean(self, v_1, v_2):
        
        distance = 0.0
        # foreach index of vectors
        for value in range(len(v_1)):
            distance += math.pow(v_1[value] - v_2[value], 2)
        return math.sqrt(distance)
            
    # Manhattan metric function
    def __manhattan(self, v_1, v_2):
        
        distance = 0.0
        
        for value in range(len(v_1)):
            distance += abs(v_1[value] - v_2[value])

        return distance

    # Minkowski metric function
    def __minkowski(self, v_1, v_2):
        
        distance = 0.0
       
        for value in range(len(v_1)):
            distance += abs(v_1[value] - v_2[value]) ** 3

        return distance ** 0.3333333333333333 
   
    # Function responsible for choosing the metric
    def __count_distance(self, v_1, v_2):

        # shorten switch case
        metrics = {'euclidean': self.__euclidean, 'manhattan': self.__manhattan, 'minkowski': self.__minkowski}

        # choose the matching metric
        metric = metrics.get(self.metric, None)

        if not metric: raise ValueError(f'The metric is inaproperiate.')
        
        return metric(v_1, v_2)    

    def fit(self, X_train_set, y_train_set):

        assert len(X_train_set) == len(y_train_set), "The length of training sets must be equal."
        
        # Train knn model with training sets
        self.X_train = X_train_set
        self.y_train = y_train_set


        if len(self.y_train) < self.k: raise ValueError(f"Expected n_samples >= n_neighbors, but... n_samples: {len(self.y_train)}, n_neighbors: {self.k}")


    def __predict_alt(self, x):
 
        decisions = {}
        for i in range(len(self.X_train)):
            if self.y_train[i][0] not in decisions:
                decisions[self.y_train[i][0]] = []
            decisions[self.y_train[i][0]].append(self.__count_distance(self.X_train[i], x))

        sums = {}

        for key in decisions.keys():
            decisions[key].sort()
            decisions[key] = decisions[key][:self.k]
            sums[key] = sum(decisions[key])

        del decisions
        
        decision = list(sums.keys())[0]
        for key, value in sums.items():
            if value < decision:
                decision = key

        return decision

    def predict(self, X):
        """ Predict function based on k-nearest neighbors """
        
        # foreach point count the distance
        predicts = [[self.__predict(x)] for x in X]

        return predicts

    def ppredict(self, X):
        """ Predict function based on k-nearest in second version """
        # get predictions 
        predictions = [[self.__predict_alt(x)] for x in X]

        return predictions
    
    
    def choose_version(self, func):
        """ Function defines the version of algorithm. """

        # default is the first version
        func_obj = self.predict
        if func != 'first':
            func_obj = self.ppredict

        return func_obj
            

    def __predict(self, x):
               
        # compute the distances
        distances = [self.__count_distance(x, x_train) for x_train in self.X_train]

        # get the sorted distances and group them by its index
        k_nearest = sorted(range(len(distances)), key=lambda f: distances[f])[:self.k]

        # get the labels based on index of training samples
        k_neighbors = [self.y_train[k_nearest[index]] for index, value in enumerate(k_nearest)]

        # to one dimmension array
        flat = [value for _list in k_neighbors for value in _list]

        # get the most common neighbors
        most_common = Counter(flat).most_common(1)[0][0]

        return most_common

    def OneVsRest(self, X_set, y_set, version='first'):
         
        assert len(X_set) == len(y_set), "The length of both - decision and input columns should be the same."
        if not isinstance(version, str): raise TypeError("Version {version} is not the string object.")
        if not ('first' in version or 'second' in version): raise ValueError(f'The value {version} of parameter is invalid.')
        
        # default mode is first
        predict = self.choose_version(version)

        # pick the kNN version
        if version.lower() == 'second':
            predict = self.choose_version(version)

        n_row = 0
        acc = 0

        for n in range(len(X_set)):

            # testing sample based on n             
            X_train_probe, y_train_probe = copy.deepcopy(X_set), copy.deepcopy(y_set)
            
            del X_train_probe[n]
            del y_train_probe[n]

            # rest are the train samples
            X_test_probe, y_test_probe = X_set[n], y_set[n]

            # take the train samples 
            self.fit(X_train_probe, y_train_probe)
            
            #  predict the x_test sample
            if version == 'second':
                predicted = predict([X_test_probe])
            else:
                # predict the X_test sample
                predicted = predict([X_test_probe])

            # if predict is succesfull
            if predicted[0] == y_test_probe:
                acc += 1
                
            n_row += 1

        print("Accuracy score: {:.2f}%,\nCovering dataset: {:.2f}".format(acc / len(X_set) * 100, len(X_set) / n_row))
        return predicted


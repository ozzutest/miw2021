import sys
import numpy as np

sys.path.append('../src')
from DataFrame import DataFrame
from kNN import kNearestNeighbors


def unpack_dataset(dataframe, n_probe):
    size = dataframe.get_shape()[0]
    if not isinstance(n_probe, int): raise ValueError('The row index is not an integer.')
    
    X_train_set = dataframe.inputs.copy()
    y_train_set = dataframe.decision_class.copy()

    X_test = X_train_set.pop(n_probe)
    y_test = y_train_set.pop(n_probe)

        
    return X_train_set, y_train_set, X_test, y_test

def is_predicted(y_test, predicted):
    if y_test == predicted[0]:
        print(f'predicted: {y_test} -> {predicted[0]}')
    else:
        print(f'not predicted: {y_test} -> {predicted[0]}')


# Initialize the dataframe object
df = DataFrame()

# Set the classificator
knn = kNearestNeighbors(k = 5, metric='euclidean')

# SET HERE ROW TO PREDICT THE SAMPLE
# get the row (input column and decision class) for predicing by index
n_probe = 12

# get train set and testing sample
X_train, y_train, x_test, y_test = unpack_dataset(df, n_probe)

# printing the sample
print(f'Testing sample: {x_test}, {y_test}')

# set the input columns and decision class to the classifier
knn.fit(X_train, y_train)
predictions = knn.predict([x_test])

# print the result
is_predicted(y_test, predictions)

# split data to inputs and decision classess
X_set, y_set = df.inputs, df.decision_class

# print decision class and input columns
#print(df.print_inputs())
#print(df.print_decision_class())
#print(df)

# first version of knn
print(f'First version of k-nearest neighbors classificator (Euclidean Metric):')
knn = kNearestNeighbors(k = 5, metric='euclidean')
knn.OneVsRest(df.inputs, df.decision_class, version='first')

print(f'First version of k-nearest neighbors classificator (Manhattan Metric):')
knn = kNearestNeighbors(k = 5, metric='manhattan')
knn.OneVsRest(df.inputs, df.decision_class, version='first')

print(f'First version of k-nearest neighbors classificator (Minkowski Metric):')
knn = kNearestNeighbors(k = 5, metric='minkowski')
knn.OneVsRest(df.inputs, df.decision_class, version='first')

# second version of knn
print(f'Second version of k-nearest neighbors classificator (Euclidean Metric):')
knn = kNearestNeighbors(k = 5, metric='euclidean')
knn.OneVsRest(df.inputs, df.decision_class, version='second')

print(f'Second version of k-nearest neighbors classificator (Manhattan Metric):')
knn = kNearestNeighbors(k = 5, metric='manhattan')
knn.OneVsRest(df.inputs, df.decision_class, version='second')

print(f'Second version of k-nearest neighbors classificator (Minkowski Metric):')
knn = kNearestNeighbors(k = 5, metric='minkowski')
knn.OneVsRest(df.inputs, df.decision_class, version='second')

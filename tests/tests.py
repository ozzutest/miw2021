import sys
import numpy as np

sys.path.append('../src')
from DataFrame import DataFrame
from kNN import kNearestNeighbors


def unpack_dataset(dataframe):
    size = dataframe.get_shape()[0]
    train_split = int(0.7 * size) # 70% percent of data as training sets
    X_train = dataframe.inputs[:train_split]
    X_test = dataframe.inputs[train_split:] # 30 % are testing sets
    Y_train = dataframe.decision_class[:train_split]
    Y_test = dataframe.decision_class[train_split:]
    print(f"Training sets: X train, Y train - {len(X_train),len(Y_train)} Testing sets: Y test, X test - {len(Y_test), len(X_test)}")
    return X_train, X_test, Y_train, Y_test


# Initialize the dataframe object

df = DataFrame()

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

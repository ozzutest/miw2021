import sys
import numpy as np

sys.path.append('../src')
from DataFrame import DataFrame
from kNN import kNearestNeighbors
        
# Initialize the dataframe object
df = DataFrame()

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

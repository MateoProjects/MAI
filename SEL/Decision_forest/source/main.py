import os
import math
from CART import * 

LAST_FEATURE_IRIS = 5
LAST_FEATURE_BALANCE = 5
LAST_FEATURE_PAGE_BLOCK = 10

def predict(data, last_value, tree):
    total_correct = 0

    print("--------- Start predictions ---------")
    for i in range(len(data)):
        predicted = tree.predict(data[i,:last_value])
        if predicted == data[i,-1]:
            total_correct += 1
    print("Accuracy:", total_correct/len(data))

def program(name, data, features):
    page = False
    if name == "iris":
        last_feature = LAST_FEATURE_IRIS
    elif name == "balance":
        last_feature = LAST_FEATURE_BALANCE
    elif name == "page":
        last_feature = LAST_FEATURE_PAGE_BLOCK
        page = True
    else:
        raise ValueError("Dataset not found")

    m = len(features)-1
    number_trees = [1, 10, 25, 50, 75, 100]
    total_features_rf = []
    random_features = [1, 3, int(math.log2(m)+1), int(math.sqrt(m))]
    print("Starting random forest")
    accuracies_rf = []
    for nt in number_trees:
        print("Using {} trees for a random forest".format(nt))
        for nf in random_features:
            forest, features = random_forest(data, range(nf), nt, page)
            accuracies_rf.append(prediction_forest(data, forest, features, last_feature))
            total_features_rf.append(features)
    print("Starting decision forest")
    accuracies_df = []
    decision_features = [int(m/4), int(m/2), int(3*m/4), 'Runif']
    total_features_df = []
    for nt in number_trees:
        print("Using {} trees for a decision forest".format(nt))
        for nf in decision_features:
            forest, features = decision_forest(data, nf, nt, page)
            print("Decision Forest with", nt, "trees and", nf, "features")
            accuracies_df.append(prediction_forest(data, forest, features, last_feature))
            total_features_df.append(features)
    print("Decision forest mean:", np.mean(accuracies_df))
    print("Total Features in decision forest used: ", total_features_df)
    print("Random forest mean:", np.mean(accuracies_rf))
    print("Total Features in random forest used: ", total_features_rf)
def read_dataset(name):
    """
    Reads a dataset from the data folder.
    """
    if name == "iris":
        data = pd.read_csv('data/iris.data', header=None).values
        return data, np.array([0,1,2,3])
    elif name == "balance":
        data = pd.read_csv('data/balance.csv', header=None).values
        # move first column to the end
        data = np.concatenate((data[:, 1:], data[:, :1]), axis=1)
        return data, np.array([0,1,2,3])
    elif name == "page":
        data = pd.read_csv('data/page-blocks.data', sep=" ", header=None).values
        return data, np.array([i for i in range(9)])
    else:
        raise ValueError("Dataset not found")
if __name__ == "__main__":
    name = input("Insert name of dataset iris, balance or page: ")
    data, features = read_dataset(name)
    program(name, data, features)
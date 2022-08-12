import numpy as np
import pandas as pd

features_used = []

def gini(labels):
    '''
    calculate gini index
    :param labels: classification of the samples
    :return: gini index
    '''
    _, counts = np.unique(labels, return_counts=True)
    return 1 - np.sum((counts/len(labels)) ** 2)


class Tree:
    def __init__(self, data, features=None, f=None):
        self.number_features = len(features)
        self.data = data
        self.right = None
        self.left = None
        self.features = features
        self.classe = None

    def build_tree(self, max_depth=100, depth=0):
        if max_depth != depth:
            thrshold_find = False
            best_gini = gini(self.data[:, -1])  # initial gini
            for feature in self.features:
                column = self.data[:, feature]
                order = np.argsort(column)
                for order_threshold in range(1, len(order)-1):
                    new_gini = (order_threshold * gini(self.data[:, -1][order][:order_threshold]) + (len(order) - order_threshold) *
                                gini(self.data[:, -1][order][order_threshold:])) / len(order)
                    if new_gini < best_gini:
                        best_gini = new_gini
                        best_attribute = feature
                        thrshold_find = True
                        best_order = order
                        best_order_threshold = order_threshold
                        threshold = (column[order][order_threshold - 1] + column[order][order_threshold]) / 2
                
            # el gini millora seguim afegint profunditat
            if thrshold_find:
                self.best_attribute = best_attribute
                self.Threshold = threshold
                self.left = Tree(self.data[best_order][:best_order_threshold], self.features)
                self.left.build_tree(max_depth=max_depth,depth=depth+1)
                self.right = Tree(self.data[best_order][best_order_threshold:], self.features)
                self.right.build_tree(max_depth=max_depth, depth=depth+1)
                features_used.append(best_attribute)
            # afegim fulla. attribut classe conté la classe max que representa     
            else:  
                self.__get_leaf()
        
        else:
            self.__get_leaf()

    def predict(self, sample):
        if self.classe is not None:
            return self.classe
        else:
            if sample[self.best_attribute] < self.Threshold:
                return self.left.predict(sample)
            else:
                return self.right.predict(sample)
          
        
    def __get_leaf(self):
            unique, counts = np.unique(self.data[:, -1], return_counts=True)
            self.classe = unique[np.argmax(counts)]  # class with maximum frequency
        
    def printTree(self):
        if self.classe is not None:
            print(self.classe)
        else:
            print("best_attribute", self.best_attribute, "threshold",self.Threshold)
            print("printing left")
            self.left.printTree()
            print("printing right")
            self.right.printTree()
           
def random_forest(data, features, num_trees, page=False):
    features_used.clear()
    forest = []
    for _ in range(num_trees):
        bootstrap = np.random.randint(0, len(data), len(data))  
        if page:
            max_depth=4
        else:
            max_depth=100
        tree = Tree(data[bootstrap], features=features) 
        tree.build_tree(max_depth=max_depth)
        forest.append(tree)

    unique_features, counts_features = np.unique(np.array(features_used), return_counts=True)
    ordered_features = np.flip(unique_features[np.argsort(counts_features)])
    return forest, ordered_features


def decision_forest(data, features, num_trees, page=False):
  
    forest = []
    features_used.clear()

    for _ in range(num_trees):
        if features == "Runif":
            features = np.random.randint(0, len(data.T -1))
        # check type of Features
        if type(features) == int:
            features = [i for i in range(features)]
        if page:
            max_depth=5
        else:
            max_depth=100
        tree = Tree(data, features=features)
        
        tree.build_tree(max_depth=max_depth)
        forest.append(tree)  # tree
    unique_features, counts_features = np.unique(np.array(features_used), return_counts=True)
    ordered_features = np.flip(unique_features[np.argsort(counts_features)])
    return forest, ordered_features


def prediction_forest(instances, forest, categories, last_feature):
    
    total_correct = 0
    init_dict = dict((el, 0) for el in categories)
    for i  in range(len(instances)):
        results = init_dict.copy()
        for tree in forest:
            prediction = tree.predict(instances[i,:last_feature])
            # check if prediction is in Results
            if prediction in results:

                results[prediction] += 1
            else: 
                results[prediction] = 1
        if instances[i, -1] == max(results, key=results.get):
            total_correct += 1
    #print("Accuracy:", total_correct/len(instances))
    return total_correct/len(instances)

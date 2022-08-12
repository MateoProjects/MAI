import pandas as pd
import numpy as np
import os
import json
from plots import *
from preprocess_balance import *
from preprocess_mushrooms import *
from preprocess_fire import *
from ruleGenerator import *

def generateDict(results):
    """
    Generate a dictionary with the results
    @param results: list of results
    @return: dictionary with the results
    """
    dictResults = {}
    results = results.unique()
    for i in range(len(results)):
        if results[i] not in dictResults:
            dictResults[str(results[i])] = []
    return dictResults


def checkElements(elements):
    """
    @param elements: list of elements
    @return: True if only one element is different from zero, False otherwise
    """
    totalGreater = 0
    for elem in elements:
        if elem > 0:
            totalGreater += 1
        if totalGreater > 1:
            return False
    if totalGreater == 0:
        return False
    return True


def checkDoubleRules(data, results, rule, dictResults, lenDataTotal):
    """
    Check rule in data
    @param data: dataframe
    @param results: list of results
    @param rule: rule to check
    @param dictResults: dictionary with the results
    @return: Conclusions that the data satisfy the rule
    """
    rows = []
    i, j, m, n, val1, val2, val3, val4 = rule[0], rule[1], rule[2], rule[3],  rule[4][0], rule[4][1], rule[4][2], rule[4][3]
    for row in range(len(data)):
        if (data[row, i] == val1) & (data[row, j] == val2) & (data[row, m] == val3) & (data[row, n] == val4):
            rows.append(row)

    elements = np.zeros(len(dictResults.keys()))
    for k in range(len(rows)):
        elements[results[rows[k]]] += 1

    checkVals = checkElements(elements)

    if checkVals:
        coverage = (len(rows)/lenDataTotal) * 100
        conclusion = (results[rows[0]], rows, coverage)
    else:
        conclusion = ("unknown", rows)
    return conclusion


def check_rules(data, results, rule, dictResults, lenDataTotal):
    """
    Check if a dataframe satisfy a list of rules
    @param data: dataframe
    @param rules: list of rules
    @return: True if the dataframe satisfy the rules, False otherwise
    """
    rows = []
    i, j, val1, val2 = rule[0], rule[1], rule[2][0], rule[2][1]
    for row in range(len(data)):
        if (data[row, i] == val1) & (data[row, j] == val2):
            rows.append(row)

    elements = np.zeros(len(dictResults.keys()))
    for k in range(len(rows)):
        elements[results[rows[k]]] += 1

    checkVals = checkElements(elements)

    if checkVals:
        coverage = (len(rows)/lenDataTotal) * 100
        conclusion = (results[rows[0]], rows, coverage)
    else:
        conclusion = ("unknown", rows)
    return conclusion


def base_rules_classifier(data, pairValues, result, dictResults, double=False): 
    """
    Classify data with base rules
    @param data: dataframe
    @param pairValues: list of pairs of values with rules
    @param result: list of results
    @param dictResults: dictionary with the results
    @return: dictionary with the rules, length of data, length of data classified, dataframe, list of results, coverage
    """
 
    na = len(data[0])
    classifiedAll = False
    indexPV = 0
    lenDataTotal = len(data)
    coverage = []
    lenDataY = [len(data)]
    while not classifiedAll and len(pairValues) > indexPV:
        rule = pairValues[indexPV]  # column i, column j, value [m,n]
        if not double:
            conclusion = check_rules(data, result, rule, dictResults, lenDataTotal)
        else:
            conclusion = checkDoubleRules(data, result, rule, dictResults, lenDataTotal)
        if conclusion[0] != "unknown":
            dictResults[str(conclusion[0])].append(rule)
            data = np.delete(data, conclusion[1], axis=0)
            result = np.delete(result, conclusion[1], axis=0)
            coverage.append(conclusion[2])
        if indexPV == len(pairValues):
            classifiedAll = True

        if len(data) == 0:
            classifiedAll = True
            print("====== All data classified ======")
        indexPV += 1
        lenDataY.append(len(data))

    lenDataX = [x for x in range(indexPV+1)]
    return dictResults, lenDataX, lenDataY, data, result, coverage


def extractUniqueValues(data):
    """
    Extract unique values from a dataframe of each column
    @param data: dataframe
    @return: list of unique values
    """
    uniqueValues = []
    for col in data:
        uniqueValues.append(data[col].unique())
    return uniqueValues


def classifyDataRemaining(data, result, dictResults, uniquePairValues):
    """
    Classify data remaining with new rules    
    @param data: dataframe
    @param result: list of results
    @param dictResults: dictionary with the results
    @param uniquePairValues: list of unique values
    @return: dictionary with the rules, length of data, length of data classified, dataframe, list of results, coverage
    """
    rules = twoInOneRule(uniquePairValues, type="int")
    print("====== Classifying the data remaining ======")
    return base_rules_classifier(data, rules, result, dictResults, double=True)


def classify(data, pairValues, result, dictResults, double=False):
    print("====== Start classification ======")
    dict_rules, lenDataX, lenDataY, data, result, coverage = base_rules_classifier(
        data, pairValues, result, dictResults)
    print("====== End classification ======")
    return dict_rules, lenDataX, lenDataY, data, result, coverage


def classificationMushrooms():
    """
    Classify mushrooms data
    """
    if not os.path.exists('data\\preprocessed_mushrooms.csv'):
        replaceValues()
    data = pd.read_csv('data\\preprocessed_mushrooms.csv', header=None)
    # read data
    result = data[0]
    dictResults = generateDict(result)
    data.drop(0, axis=1, inplace=True)
    uniqueValues = extractUniqueValues(data)
    pairValues = pairOfValue(uniqueValues)
    data = np.array(data)
    result = np.array(result)
    dict_rules, lenDataX, lenDataY, data, result, coverage = classify(
        data, pairValues, result, dictResults)
    if len(result) != 0:
        # data not classified
        dict_rules, lenDataX, lenDataY, data, result, coverage = classifyDataRemaining(
            data, result, dict_rules, uniqueValues)

    plotLen(lenDataX, lenDataY, "Results\\length_mushrooms.png")
    plotCoverage(coverage)
    json.dump(dict_rules, open("Results\\rules_mushrooms.json", "w"))


def classificationFire():
    """
    Classify fire data
    """
    if not os.path.exists('data\\preprocessFire.csv'):
        preprocessFire()
    data = pd.read_csv('data\\preprocessFire.csv', header=None)
    result = data[13]
    # generate dictionary with the results like {0: [], 1: [], 2: []}
    dictResults = generateDict(result)
    data.drop(13, axis=1, inplace=True)
    uniqueValues = extractUniqueValues(data)
    pairValues = pairOfValue(uniqueValues, type="int")
    data = np.array(data)
    result = np.array(result)
    dict_rules, lenDataX, lenDataY, data, result, coverage = classify(
        data, pairValues, result, dictResults)
    if len(result) != 0:
        # data not classified
        dict_rules, lenDataX, lenDataY, data, result, coverage = classifyDataRemaining(
            data, result, dict_rules, uniqueValues)
    plotCoverage(coverage)
    plotLen(lenDataX, lenDataY, "Results\\fire_classified.png")
    json.dump(dict_rules, open("Results\\rules_fire.json", "w"))


def classificationBalance():
    """
    Classify Balance data
    """
    if not os.path.exists('data\\preprocessed_balance.csv'):
        preprocessBalance()
    data = pd.read_csv('data\\preprocessed_balance.csv', header=None)
    result = data[0]
    dictResults = generateDict(result)
    data.drop(0, axis=1, inplace=True)
    uniqueValues = extractUniqueValues(data)
    pairValues = pairOfValue(uniqueValues, type="int")
    data = np.array(data)
    result = np.array(result)
    dict_rules, lenDataX, lenDataY, data, result, coverage = classify(
        data, pairValues, result, dictResults)
    if len(result) != 0:
        # data not classified
        dict_rules, lenDataX, lenDataY, data, result, coverage = classifyDataRemaining(
            data, result, dict_rules, uniqueValues)
        print("====== End data remaining classification ======")
    plotLen(lenDataX, lenDataY, "Results\\balance_classified.png")
    plotCoverage(coverage)
    json.dump(dict_rules, open("Results\\balance.json", "w"))



def predictRow(row, dict_rules, result, double=False):
    """
    Predict the result of a row
    @param row: row to predict
    @param dict_rules: dictionary with the rules
    @param result: list of results
    @param double: if the data is double
    @return: predicted result
    """
    for key in dict_rules.keys():
        for rule in dict_rules[key]:
            if not double:
                i, j, val1, val2 = rule[0], rule[1], rule[2][0], rule[2][1]
                if (row[i] == val1) & (row[j] == val2):
                    if key == str(result):
                        return 1
                    else:
                        return 0
    return 0                    

def printLenDict(dict_rules):
    """
    Print the length of each rule
    """
    for key in dict_rules.keys():
        print("For class:",key, "the total rules are:" ,len(dict_rules[key]))

def predict(data, dict_rules, results, double=False):
    """
    Predict the result of the data
    @param data: dataframe
    @param dict_rules: dictionary with the rules
    @return: list of predicted values
    """
    
    correctPredictions = 0
    for i in range(len(data)):
        row = data.iloc[i]
        correctPredictions += predictRow(np.array(row), dict_rules, results[i], double)
    
    print("Len of data is", len(data), "\nTotal correct predictions:", correctPredictions, "\nAccuracy:", correctPredictions/len(data))
        
def test_classification(name):
    """
    Test classification of data
    @param name: name of the data
    """
    if name == "mushrooms":
        rules = json.load(open("Results\\rules_mushrooms.json", "r"))
        printLenDict(rules)
        data_test = pd.read_csv('data\\preprocessed_mushrooms_test.csv', header=None)
        result_test = data_test[0]
        data_test.drop(0, axis=1, inplace=True)
        predict(data_test, rules, result_test, double=False)
    elif name == "fire":
        rules = json.load(open("Results\\rules_fire.json", "r"))
        printLenDict(rules)
        data_test = pd.read_csv('data\\preprocessFire_test.csv', header=None)
        result_test = data_test[13]
        data_test.drop(13, axis=1, inplace=True)
        predict(data_test, rules, result_test, double=False)
    elif name == "balance":
        rules = json.load(open("Results\\balance.json", "r"))
        printLenDict(rules)
        data_test = pd.read_csv('data\\preprocessed_balance_test.csv', header=None)
        result_test = data_test[0]
        data_test.drop(0, axis=1, inplace=True)
        predict(data_test, rules, result_test, double=True)
        


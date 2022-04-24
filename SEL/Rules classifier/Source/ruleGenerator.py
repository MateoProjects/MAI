def generateCombinations(list1, list2, type):
    """_
    Generates a combinations of two lists
    @param list1: list
    @param list2: list
    @return: list of combinations
    """
    combinations = []
    for i in list1:
        for j in list2:
            if type == "str":
                combinations.append([i, j])
            else:
                combinations.append([int(i), int(j)])
    return combinations


def generateCombinationsDouble(list1, list2, list3, list4, type):
    """
    Generates a combinations of four lists
    @param list1: list
    @param list2: list
    @param list3: list
    @param list4: list
    @param type: str or int
    @return: list with all possible combinations
    """
    combinations = []
    for i in list1:
        for j in list2:
            for m in list3:
                for n in list4:
                    if type == "str":
                        combinations.append([i, j, m, n])
                    else:
                        combinations.append([int(i), int(j), int(m), int(n)])

    return combinations


def pairOfValue(uniqueValues: list, type="str"):
    """
    Generates a combinations of unique values
    @param uniqueValues: list
    @param type: str or int
    @return: list with all possible combinations
    """

    pairOfValues = []
    for i in range(len(uniqueValues)):
        for j in range(i+1, len(uniqueValues)):
            for k in generateCombinations(uniqueValues[i], uniqueValues[j], type):
                pairOfValues.append((i, j, k))

    return pairOfValues


def twoInOneRule(uniqueValues: list, type="str"):
    """
    Generates a combinations of unique values with four values in each combination
    @param uniqueValues: list
    @param type: str or int
    @return: list with all possible combinations
    """
    pairOfRules = []
    for i in range(len(uniqueValues)):
        for j in range(i+1, len(uniqueValues)):
            for m in range(j+1, len(uniqueValues)):
                for n in range(m + 1, len(uniqueValues)):
                    for k in generateCombinationsDouble(uniqueValues[i], uniqueValues[j], uniqueValues[m], uniqueValues[n], type):
                        pairOfRules.append((i, j, m, n, k))

    return pairOfRules

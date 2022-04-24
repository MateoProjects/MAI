import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

dictBalance = {"L": 0, "B": 1, "R":2}
dataReplace = []





def preprocessBalance():
    """
    Apply preprocessing to balance dataset
    """
    data = pd.read_csv('data\\balance-scale.data', header=None)
    for i in range(len(data)):
        key = data[0][i]
        dataReplace.append(dictBalance[key])
    data[0] = dataReplace
    train, test = train_test_split(data, test_size=0.2)
    train.to_csv('data/preprocessed_balance.csv', index=False, header=False)
    test.to_csv('data/preprocessed_balance_test.csv', index=False, header=False)

import pandas as pd
from sklearn.model_selection import train_test_split


dictFire = {"fire": 0, "not fire": 1}
dataReplace = []
def preprocessFire():
    data = pd.read_csv('data\\fire_dataset.csv', header=None)
    for i in range(len(data)):

        key = " ".join(data[13][i].split())
        dataReplace.append(dictFire[key])
    data[13] = dataReplace
    #data.to_csv('data/preprocessFire.csv', index=False, header=False)
    train, test = train_test_split(data, test_size=0.2)
    train.to_csv('data\\preprocessFire.csv', index=False, header=False)
    test.to_csv('data\\preprocessFire_test.csv', index=False, header=False)



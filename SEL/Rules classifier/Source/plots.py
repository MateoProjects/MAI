import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import PercentFormatter


def plotLen(lenDataX, lenDataY, name):
    """
    Plot len of data
    @param lenDataX: len of data X
    @param lenDataY: len of data Y
    @param name: name of data
    """
    # plot the length of the data
    plt.plot(lenDataX, lenDataY)
    plt.savefig(name)

def plotCoverage(coverage):
    """
    Plot coverage of data
    @param coverage: coverage of data
    @param name: name of data
    """
    max = np.max(coverage)
    for i in range(5):
        print("Rule:", i, "Coverage:", coverage[i])
    print("Max coverage:", max)

def plotDataMushroom():
    """
    Plot data mushroom
    """
    data = pd.read_csv('data/preprocessed_mushrooms.csv', header=None)
    #iter columns
    p, e = 0, 0
    for row in data.iterrows():
        if row[1][0] == 1:
            p += 1
        else:
            e += 1
    # plot bar chart
    plt.bar(['poisonous', 'edible'], [p, e], color=['red', 'green'])
    plt.savefig('data/mushroom_bar.png')
    plt.show()

def plotFire():
    """
    Plot data fire
    """
    data = pd.read_csv('data/preprocessFire.csv', header=None)
    data2 = pd.read_csv('data/preprocessFire_test.csv', header=None)
    data = data.append(data2)
    f, nf = 0, 0
    for row in data.iterrows():
        if row[1][13] == 1:
            nf += 1
        else:
            f += 1
   

    plt.bar(['fire', 'not fire'], [f, nf], color=['red', 'green'])
    plt.savefig('data/fire_bar.png')
    plt.show()


def plotBalance():
    """
    Balance data
    """
    data = pd.read_csv('data/preprocessed_balance.csv', header=None)
    data2 = pd.read_csv('data/preprocessed_balance_test.csv', header=None)
    data = data.append(data2)
    # dictBalance = {"L": 0, "B": 1, "R":2}

    L, B, R = 0, 0, 0
    for row in data.iterrows():
        if row[1][0] == 0:
            L += 1
        elif row[1][0] == 1:
            B += 1
        else:
            R += 1
    plt.bar(['Left', 'Balance', 'Right'], [L, B, R], color=['red', 'green', 'blue'])
    plt.savefig('data/balance_bar.png')


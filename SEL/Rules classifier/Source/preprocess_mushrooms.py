import pandas as pd
from plots import *
from sklearn.model_selection import train_test_split

dict_result = {'e': 0, 'p': 1}
dict_capShape = {
    "b": "bell", "c": "conical ",  "x": "convex",  "f": "flat",
    "k": "knobbed", "s": "sunken"
}
dict_capSurface = {
    "f": "fibrous", "g": "grooves", "y": "scaly", "s": "smooth"
}
dict_capColor = {
    "n": "brown", "b": "buff", "c": "cinnamon", "g": "gray", "r": "green", "p": "pink", "u": "purple", "e": "red", "w": "white", "y": "yellow"
}
dictBruises = {
    "t": "bruises", "f": "no"
}
dict_odor = {
    "a": "almond", "l": "anise", "c": "creosote", "y": "fishy", "f": "foul", "m": "musty", "n": "none", "p": "pungent", "s": "spicy"
}
dict_gillAttachment = {
    "a": "attached", "d": "descending", "f": "free", "n": "notched"
}
dict_gillSpacing = {
    "c": "close", "w": "crowded", "d": "distant"
}
dict_gillSize = {
    "b": "broad", "n": "narrow"
}
dict_gillColor = {
    "k": "black", "n": "brown", "b": "buff", "h": "chocolate", "g": "gray", "r": "green", "o": "orange", "p": "pink", "u": "purple", "e": "red", "w": "white", "y": "yellow"   
}
dict_stalkShape = {
    "e": "enlarging", "t": "tapering"
}
dict_stalkRoot = {
    "b": "bulbous", "c": "club", "u": "cup", "e": "equal", "z": "rhizomorphs", "r": "rooted", "?": "missing"
}
dict_stalkSurfaceAboveRing = {
    "f": "fibrous", "y": "scaly", "k": "silky", "s": "smooth"
}
dict_stalkSurfaceBelowRing = {
    "f": "fibrous", "y": "scaly", "k": "silky", "s": "smooth"    
}
dict_stalkColorAboveRing = {
    "n": "brown", "b": "buff", "c": "cinnamon", "g": "gray", "o": "orange", "p": "pink", "e": "red", "w": "white", "y": "yellow"
}
dict_stalkColorBelowRing = {
    "n": "brown", "b": "buff", "c": "cinnamon", "g": "gray", "o": "orange", "p": "pink", "e": "red", "w": "white", "y": "yellow"
}
dict_veilType = {
    "p": "partial", "u": "universal"
}
dict_veilColor = {
    "n": "brown", "o": "orange", "w": "white", "y": "yellow"
}
dict_ringNumber = {
    "n": "none", "o": "one", "t": "two"
}
dict_ringType = {
    "c": "cobwebby", "e": "evanescent", "f": "flaring", "l": "large", "n": "none", "p": "pendant", "s": "sheathing", "z": "zone"
}
dict_sporePrintColor = {
    "k": "black", "n": "brown", "b": "buff", "h": "chocolate", "r": "green", "o": "orange", "u": "purple", "w": "white", "y": "yellow"
}
dict_population = {
    "a": "abundant", "c": "clustered", "n": "numerous", "s": "scattered", "v": "several", "y": "solitary"
}
dict_habitat = {
    "g": "grasses", "l": "leaves", "m": "meadows", "p": "paths", "u": "urban", "w": "waste", "d": "woods"
}  
listOfDicts = [dict_result,dict_capShape, dict_capSurface, dict_capColor, dictBruises, dict_odor, dict_gillAttachment, dict_gillSpacing, dict_gillSize, dict_gillColor, dict_stalkShape, dict_stalkRoot, dict_stalkSurfaceAboveRing, dict_stalkSurfaceBelowRing, dict_stalkColorAboveRing, dict_stalkColorBelowRing, dict_veilType, dict_veilColor, dict_ringNumber, dict_ringType, dict_sporePrintColor, dict_population, dict_habitat]



def replaceValues():
    """
    Replace letter by their corresponding word in the dataframe
    """
    data = pd.read_csv('data/agaricus-lepiota.data', header=None)
    #iter columns
    index = 0
    for col in data:
        dict_index = listOfDicts[index]

        for row in range(len(data[col])):
            #iter dicts
            data[col][row] = dict_index[data[col][row]]
        index += 1
    # save data as csv
    #data.to_csv('data/preprocessed_mushrooms.csv', index=False, header=False)
    train, test = train_test_split(data, test_size=0.2)
    train.to_csv('data\\preprocessed_mushrooms.csv', index=False, header=False)
    test.to_csv('data\\preprocessed_mushrooms_test.csv', index=False, header=False)

# edible = 0, poisonous = 1

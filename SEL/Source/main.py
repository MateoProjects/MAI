from classifiers import * 

    
    
    
    
if __name__ == "__main__":
    val = input("Insert 0 for mushrooms dataset, 1 for fire dataset, 2 for balance dataset else -1: ")
    if val == "0":
        classificationMushrooms()
        test_classification("mushrooms")
    elif val == "1":
        classificationFire()
        test_classification("fire")
    elif val == "2":
        classificationBalance()
        test_classification("balance")
    else:
        pass
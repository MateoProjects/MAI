# This Python3 script removes repetitions from the "our_resources" files

drug = open("../data/resources/drug.txt", 'rw', encoding='utf-8').readlines()
drug_n = open("../data/resources/drug_n.txt", 'rw', encoding='utf-8').readlines()
brand = open("../data/resources/brand.txt", 'rw', encoding='utf-8').readlines()
groups = open("../data/resources/group.txt", 'rw', encoding='utf-8').readlines()
drug = [x.strip().lower() for x in drug]
drug_n =  [x.strip().lower() for x in drug_n]
brand = [x.strip().lower() for x in brand]
groups = [x.strip().lower() for x in groups]

drugBank = open("../data/resources/drugBank.txt", 'r', encoding='utf-8').readlines()
drugBank = [x.strip().lower() for x in drugBank]

for line in drugBank:
    typeDrug = line.split("|")[2]
    nameDrug = line.split("|")[0]
    if typeDrug == "brand" and nameDrug not in brand:
        brand.append(nameDrug)
    elif typeDrug == "group" and nameDrug not in groups:
        groups.append(nameDrug)
    elif typeDrug == "drug" and nameDrug not in drug and nameDrug not in drug_n:
        drug.append(nameDrug)

files = ["drug.txt", "drug_n.txt", "brand.txt", "group.txt"]
listToSave = [drug, drug_n, brand, groups]
for i in range(4):
    textFile = open("resources/"+files[i], "w", encoding="utf-8")
    for line in listToSave[i]:
        textFile.write(line + "\n")
    textFile.close()

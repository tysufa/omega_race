levels=[]
import csv
with open("levels.csv", "r") as fichier:
    ligne = csv.reader(fichier, delimiter=',', quotechar='|')
    for case in ligne :
        levels.append(case)
levels.pop(0)
for i in range(len(levels)):
    levels[i].pop(0)
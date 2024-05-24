'''
Created on 24 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
from myLib.fiwareAnswer import FiwareAnswer
from myLib.readGtfs import ReadGtfs
upv = Fiware()
reader=ReadGtfs()
ls=reader.readGtfsStops()
print("Readed entities")
upv.printListOfDicts(ls)

print("Uploading list of entities")
l=upv.uploadListOfEntities(ls)

print("Results")
print(l)


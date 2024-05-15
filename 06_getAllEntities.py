'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
from myLib.fiwareAnswer import FiwareAnswer
upv=Fiware()
r:FiwareAnswer=upv.getAllEntities()
#upv.printListOfDicts(r)

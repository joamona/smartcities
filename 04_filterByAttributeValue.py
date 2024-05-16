'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()
#upv.filterByAttributeValue(attributeName='accuracy', attributeValue=3, operator='>')
le=upv.filterByUserAndProperties(etype='PPPP', fields={'accuracy':3.5})
#upv.printListOfDicts(le)
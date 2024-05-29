'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()
r=upv.filter(type='Gate',fieldsValuesDict={'username':'joamona'})
upv.deleteListOfEntities(listOfEntities=r.resultingEntities)

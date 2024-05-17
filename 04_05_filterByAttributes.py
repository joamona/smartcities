'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()
le=upv.filter(fieldsValuesDict={"username":"joamona","accuracy":3})

'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()

upv.filterBySeveralAttributeValueConditions(andConditions='accuracy>3;accuracy<4')
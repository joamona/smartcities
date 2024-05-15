'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware

upv = Fiware()
print(upv.createUrn(etype='Gate', ename='K2'))
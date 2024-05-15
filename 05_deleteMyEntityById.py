'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()
upv.deleteMyEntityById(entity_id=upv.createUrn(etype='Dummy2', ename='K2'))

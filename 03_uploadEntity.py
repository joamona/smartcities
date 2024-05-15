'''
Created on 4 jul 2023

@author: joamona
'''

from myLib.fiware import Fiware
upv=Fiware()
dummy=upv.createEntity(etype='Dummy3', ename='K4')
upv.uploadEntity(entity=dummy)
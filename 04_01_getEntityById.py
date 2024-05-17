'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
from myLib.fiwareAnswer import FiwareAnswer
upv=Fiware()

fa:FiwareAnswer=upv.getEntityById(entity_id=upv.createUrn(etype='Dummy3', ename='K3'))
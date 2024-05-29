'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware

upv=Fiware()
attributes={
    'username':{'type':'Text', 'value':'juan'}, 
    'accuracy':{'type':'Float', 'value':2.333}
}
upv.updateEntityAttributes(entityId='urn:ngsi-ld:joamona:Dummy2:K2',attributes=attributes)
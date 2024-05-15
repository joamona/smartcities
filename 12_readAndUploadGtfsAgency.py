'''
Created on 24 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
from myLib.fiwareAnswer import FiwareAnswer
from myLib.readGtfs import ReadGtfs
upv = Fiware()
reader=ReadGtfs()
agency=reader.readGtfsAgency()
upv.uploadEntity(entity=agency)

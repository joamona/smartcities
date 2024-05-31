'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.readCsv import ReadCsv
from myLib.fiware import Fiware

fileName='C:\gescont\smartcities\co2sensor.csv'
csv=ReadCsv(csvFileName=fileName, csvSeparator=';', csvHasHeader=True)
csv.printConfig()
csv.printData()

upv=Fiware()

csvEntities=upv.createCsvEntities(etype="sensor", csvData=csv.csvData, csvHeader=csv.csvHeader,
                                  eNameFieldName='ID',
                                  latLonFieldNames=['Longitude','Latitude'])


'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.readCsv import ReadCsv
from myLib.fiware import Fiware

fileName='/home/joamona/www/apps/desweb/smartcities/upv_access_points.csv'
csv=ReadCsv(csvFileName=fileName, csvSeparator=',', csvHasHeader=True)
csv.printConfig()
csv.printData()

upv=Fiware()

csvEntities=upv.createCsvEntities(etype="Gate", csvData=csv.csvData, csvHeader=csv.csvHeader,
                                  eNameFieldName='PID',
                                  latLonFieldNames=['Longitude','Latitude'])

status=upv.uploadListOfEntities(csvEntities)
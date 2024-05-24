'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.readCsv import ReadCsv

fileName='/home/joamona/docker/smartcities/upv_access_points.csv'
csv=ReadCsv(csvFileName=fileName, csvSeparator=',', csvHasHeader=True)
csv.printConfig()
csv.printData()

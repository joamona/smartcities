'''
Created on 2 jun 2023

@author: joamona
'''
import fiware, readCsv

url = 'https://smartcities.upvusig.car.upv.es/fiware/'
user = 'joamona'
upv = fiware.Fiware(url, user)
#print(upv.getVersion())

#e=upv.createGeoEntity(etype='Gate3', ename='A', 
#                    coordinates=[-0.34722055,39.4831925])

#upv.uploadEntity(e)

#e=upv.getAllEntities()
#upv.printDict(d=e)
fileName='/home/joamona/www/apps/desweb/smartcities/upv_access_points.csv'
csv=readCsv.ReadCsv(csvFileName=fileName, csvSeparator=',', csvHasHeader=True)
csv.printConfig()
csv.printData()


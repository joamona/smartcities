'''
Created on 2 jun 2023

@author: joamona
'''
import fiware as smart

url = 'https://smartcities.upvusig.car.upv.es/fiware/'
user = 'joamona'
upv = smart.Fiware(url, user)
upv.url=url
upv.user=user
print(upv.getVersion())


dummy=upv.createEntity(etype='Dummy2', ename='K2')

status = upv.uploadEntity(entity=dummy)
print(status)

print(upv.getAllEntities())

print(upv.countEntities())

print(upv.deleteEntity('Dummy2','K2'))

upv.deleteAllEntities()
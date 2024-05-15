'''
Created on 2 jun 2023

@author: joamona
'''
import json
import requests
import inspect

#class Fiware

class Fiware():
    def __init__(self, url, user, printInfo=True):
        #attributes
        self.url=url
        self.user=user
        self.version='/version'
        self.entities = '/v2/entities'
        self.urlEntities=self.url + self.entities
        self.headers={'Content-Type': 'application/json'}
        self.requesResult = None
        self.printInfo=printInfo
        self.csvHeader:list=None
        self.csvData:list=None

    def printRequestResult(self):
        if self.printInfo:
            print("Status code: " + str(self.requesResult.status_code))
            print("Text message: " + self.requesResult.text)
        
    def printMethodName(self,methodName):
        if self.printInfo:
            print(methodName)
            
    def printDict(self,d):
        print(json.dumps(d, indent=4))
        
    def printJson(self,js):
        self.printDict(d=js.json())

    def getVersion(self):
        url=self.url + self.version
        res = requests.get(url)
        return json.dumps(res.json(), indent=4)
    
    def createEntity(self,etype,ename):
        urn = f'urn:ngsi-ld:{self.user}:{etype}:{ename}'
        payload={
            'id': urn,
            'type':etype,
            'name':{
                'type':'Text',
                'value':ename
                }
            }
        entity={
            'type':etype,
            'name':ename,
            'payload':payload
            }
        print(json.dumps(entity, indent=4))
        return entity
    
    def uploadEntity(self, entity):
        self.requesResult=requests.post(
            self.urlEntities,
            headers=self.headers,
            data=json.dumps(entity['payload'])
            )
        print(inspect.stack()[0][3])#imprime el nombre del método actual
        self.printRequestResult()
        return f'[{self.requesResult.status_code}]'
    
    def getAllEntities(self):
        self.requesResult = requests.get(self.urlEntities)
        if self.requesResult.status_code >= 200 and self.requesResult.status_code < 300:
            return self.requesResult.json()
        else:
            self.printRequestResult()
            return f'[{self.requesResult.status_code}]'

    def countEntities(self):
        parameters={'options':'count'}
        r=requests.get(self.urlEntities,params=parameters)
        try:
            count = int(r.headers['Fiware-Total-Count'])
        except:
            count = None
        return count
    
    def deleteEntity(self,etype,ename):
        entity_id = self.createEntity(etype, ename)
        print(entity_id)
        if self.user not in entity_id:
            print('You are not allowed to delete other user entities')
            return 
        url = self.urlEntities + '/' + entity_id
        self.requesResult=requests.delete(url)
        self.printRequestResult()
        return f'[{self.requesResult.status_code}]'
    
    def deleteEntityById(self,entity_id):
        if self.user not in entity_id:
            print('You are not allowed to delete other user entities')
            return 
        url = self.urlEntities + '/' + entity_id
        self.requesResult=requests.delete(url)
        self.printRequestResult()
        return f'[{self.requesResult.status_code}]'
    
    
    def deleteAllEntities(self):
        e=self.getAllEntities()
        for en in e:
            print(self.deleteEntityById(en['id']))
        
    def createGeoEntity(self,etype,ename,coordinates):
        #coordinates=[longitude, latitude]
        urn = urn = f'urn:ngsi-ld:{self.user}:{etype}:{ename}'
        payload={
            'id':urn,
            'type':etype,
            'name':{
                'type':'text',
                'value':ename
                },
            'location':{
                'type':'geo:json',
                'value':{
                    'type':'Point',
                    'coordinates':coordinates
                    }
                }
            }
        entity={
            'type':etype,
            'name':ename,
            'payload':payload
            }
        self.printDict(d=entity)
        return entity
    


        
        
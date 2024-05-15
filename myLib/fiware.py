'''
Created on 2 jun 2023

@author: joamona
'''
import os
import json
import inspect
import webbrowser

import folium
import requests
#class Fiware

from myLib.fiwareAnswer import FiwareAnswer

class Fiware():
    def __init__(self, url='https://smartcities.upvusig.car.upv.es/fiware', user='joamona', printInfo=True):
        #attributes
        self.url=url
        self.user=user
        self.entities = '/v2/entities'
        self.urlEntities=self.url + self.entities
        self.headers={'Content-Type': 'application/json'}
        self.requesResult = None
        self.printInfo=printInfo

    def request(self,url):
        pass

    def printRequestResult(self):
        if self.printInfo:
            print('url: ' + self.url)
            print("Status code: " + str(self.requesResult.status_code))
            print("Text message: " + self.requesResult.text)
        
    def printMethodName(self,methodName):
        if self.printInfo:
            print(methodName)
            
    def printDict(self,d):
        print(json.dumps(d, indent=4))
    
    def printListOfDicts(self,l):
        for d in l:
            self.printDict(d) 
            
    def printJson(self,js):
        self.printDict(d=js.json())

    def getVersion(self):
        url=self.url + '/version'
        res = requests.get(url)
        return json.dumps(res.json(), indent=4)
    
    def createUrn(self,etype,ename):
        urn = f'urn:ngsi-ld:{self.user}:{etype}:{ename}'
        return urn
    
    def createEntity(self,etype,ename, attributes={}):
        """
        Atributes should be in the format:
        attributes={
            "accuracy": {
                "type": "Float",
                "value": 3.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        }
        """
        payload={
            'id': self.createUrn(etype, ename),
            'type':etype,
            'name':{
                'type':'Text',
                'value':ename
                }
            }
        for key, value in attributes.items():
            payload[key]=value
            
        entity={
            'type':etype,
            'name':ename,
            'payload':payload
            }
        print(json.dumps(entity, indent=4))
        return entity
    
    def createGeoEntity(self,etype,ename,coordinates, attributes={}):
        #coordinates=[longitude, latitude]
        
        payload={
            'id':self.createUrn(etype, ename),
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
        print('attributes',attributes)
        for key, value in attributes.items():
            payload[key]=value
        print('payload')
        print(payload)
        entity={
            'type':etype,
            'name':ename,
            'payload':payload
            }
        self.printDict(d=entity)
        return entity
    
    def uploadEntity(self, entity):
        """
        Fíjate que lo que se sube e el payload del diccionario
        """
        print('Upload entity')
        self.requesResult=requests.post(
            self.urlEntities,
            headers=self.headers,
            data=json.dumps(entity['payload'])
            )
        fa=FiwareAnswer(answer=self.requesResult,entity=entity)
        return fa
    
    def uploadListOfEntities(self,l):
        lStatus=[]
        n=len(l)
        for i in range(len(l)):
            print(f'Uploading entity: {i} of {n}')
            fa=self.uploadEntity(l[i])
            lStatus.append(fa)
        return lStatus
    
    def filterByType(self, etype:str, limit=1000):
        self.url=self.urlEntities + '?type=' + etype + '&limit=' + str(limit)  + '&options=count'
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa 

    def filterByIdPattern(self, idSubString:str, limit=1000):
        '^.*Test.*$'
        self.url=self.urlEntities + '?idPattern=^.*' + idSubString + '.*$' + '&limit=' + str(limit)  + '&options=count'
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa

    def filterByIdPatternAndType(self, idSubString:str,etype:str, limit=1000):
        '^.*Test.*$'
        self.url=self.urlEntities + '?idPattern=^.*' + idSubString + '.*$' + '&type=' + etype +'&limit=' + str(limit)  + '&options=count'
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa

    
    def filterByUserAndProperties(self, etype=None, fields=None, limit=1000)->FiwareAnswer:
        """
        This method gets all the user entities
        makes several requests to get 1000 entities
        and join them in one result
        """
        parameters = {
            'idPattern': self.user,
            'offset': 0,
        }
        parameters['limit'] = limit

        if etype is not None:
            parameters['type'] = etype

        if fields is not None and isinstance(fields, dict):
            for key, value in fields.items():
                parameters['q'] = f'{key}=={value}'
        print("filterByUserAndProperties. Current parameters:")
        print(parameters.items())
        
        page = 0
        entities = []
        while True:
            response = requests.get(self.urlEntities, params=parameters)
            fa:FiwareAnswer=FiwareAnswer(answer=response)
            if len(response.json()) == 0:
                break
            entities += response.json()
            page += 1
            parameters['offset'] = page * limit
        fa=FiwareAnswer(answer=response)
        fa.setResultingEntities(resultingEntities=entities)
        return fa
    """
    def filterByAttributeValue(self, attributeName:str, attributeValue, operator='==', limit=1000):
        #Operator can be >, ==, <
        
        self.url=self.urlEntities + '?q=' + attributeName + operator + str(attributeValue) + '&limit=' + str(limit) + '&options=count'
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa
    """
    
    def filterBySeveralAttributeValueConditions(self, andConditions:str, limit=1000):
        """
        conditions must be like: 'accuracy>2;accuracy<5;mode==8'
        Means accuracy > 2 and accuracy <5 and mode ==8
        There is not OR condition.
        """
        self.url=self.urlEntities + '?q=' + andConditions + '&limit=' + str(limit) + '&options=count'
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer( answer=self.requesResult)
        return fa
    """
    #this does not retrieve more than 1000 entities          
    def getAllEntities(self, limit=1000):
        url=self.urlEntities + '?limit=' + str(limit) + '&options=count'
        fa = FiwareAnswer(requests.get(url)) 
        return fa
    """    
    """
    #this does not retrieve more than 1000 entities 
    def getAllUserEntities(self,user=None, limit=1000):

        print("Getting all user entities")
        if user==None:
            user=self.user
        fa:FiwareAnswer=self.filterByIdPattern(user, limit)
        return fa
    """
    
    def getEntityById(self,entity_id):
        url=self.urlEntities + '/' + entity_id
        self.requesResult=requests.get(url)
        return FiwareAnswer(answer=self.requesResult)

    def countEntities(self):
        parameters={'options':'count'}
        r=requests.get(self.urlEntities,params=parameters)
        try:
            count = int(r.headers['Fiware-Total-Count'])
        except:
            count = None
        return count
    
    def deleteMyEntityEntityByEtypeEname(self,etype,ename):
        entity_id = self.createEntity(etype, ename)
        print(entity_id)
        if self.user not in entity_id:
            print('You are not allowed to delete other user entities')
            return 
        url = self.urlEntities + '/' + entity_id
        self.requesResult=requests.delete(url)
        self.printRequestResult()
        return f'[{self.requesResult.status_code}]'
    
    def deleteMyEntityById(self,entity_id):
        """
        There is not a feature in Fiware to delete several entities at once
        It is necessary select them and remove them one by one
        """
        if self.user not in entity_id:
            print('You are not allowed to delete other user entities')
            return 
        url = self.urlEntities + '/' + entity_id
        self.requesResult=requests.delete(url)
        fa:FiwareAnswer=FiwareAnswer(self.requesResult)
        return fa
    
    
    def deleteAllMyEntities(self):
        fa1:FiwareAnswer=self.filterByUserAndProperties()
        print("Deleting entities one by one")
        n=len(fa1.resultingEntities)
        results:[FiwareAnswer]=[]
        for i in range(n):
            print(f'Deleting entity {i+1} of {n}')
            en=fa1.resultingEntities[i]
            #pay attention. Here the payload field is not
            #when you upload an entity you get the id as en['payload']['id']
            #but when you download an entity you simply use en['id']
            fa:FiwareAnswer=self.deleteMyEntityById(en['id'])
            fa.entity=en
            results.append(fa)

    def createCsvEntities(self, etype, csvData:list, csvHeader:list):
        #csvData es una lista de listas 
        #csv header is: ['PID', 'LONGITUDE', 'LATITUDE', 'ACCURACY', 'DATE']
        #ename es PID
        
        specialFields=['PID', 'LONGITUDE', 'LATITUDE']
        
        csvEntities=[]
        for record in csvData:
            attributes={}
            for index, fieldName in enumerate(csvHeader):
                if not fieldName in specialFields:
                    value=record[index]
                    if isinstance(value, float):
                        attributes[fieldName.lower()]={
                            'type': 'Float',
                            'value': value
                            }
                    elif isinstance(value, int):
                        attributes[fieldName.lower()]={
                            'type': 'Integer',
                            'value': value
                            }
                    else:
                        attributes[fieldName.lower()]={
                            'type': 'Text',
                            'value': value
                            }   
            geoEntity=self.createGeoEntity(etype=etype, 
                                           ename=record[0], 
                                           coordinates=[record[1],record[2]],
                                           attributes=attributes)
    
            csvEntities.append(geoEntity)
        return csvEntities
        
        
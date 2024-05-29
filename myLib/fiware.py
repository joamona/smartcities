"""
Created on 2 jun 2023

@author: joamona
"""
import os
import json
import inspect
import webbrowser

import folium
import requests
#class Fiware

from myLib.fiwareAnswer import FiwareAnswer
from myLib import fiwareSettings

class Fiware():
    def __init__(self, url=fiwareSettings.SERVER_URL, user=fiwareSettings.USERNAME, printInfo=True):
        #attributes
        self.url=url
        self.user=user
        self.entities = "/v2/entities"
        self.urlEntities=self.url + self.entities
        self.headers={"Content-Type": "application/json"}
        self.requesResult = None
        self.printInfo=printInfo
        if self.printInfo:
            print("Fiware class. __init__")

    def request(self,url):
        pass

    def printRequestResult(self):
        if self.printInfo:
            print("Fiware class. printRequestResult")
            print("url: " + self.url)
            print("Status code: " + str(self.requesResult.status_code))
            print("Text message: " + self.requesResult.text)
        
    def printMethodName(self,methodName):
        if self.printInfo:
            print("Fiware class. printMethodName")
            print(methodName)
            
    def printDict(self,d):
        if self.printInfo:
            print("Fiware class. printDict")
        print(json.dumps(d, indent=4))
    
    def printListOfDicts(self,l):
        if self.printInfo:
            print("Fiware class. printListOfDicts")        
        for d in l:
            self.printDict(d) 
            
    def printJson(self,js):
        if self.printInfo:
            print("Fiware class. printJson")       
        self.printDict(d=js.json())

    def getVersion(self):
        url=self.url + "/version"
        res = requests.get(url)
        r=json.dumps(res.json(), indent=4)
        if self.printInfo:
            print("Fiware class. getVersion")
            print(f"Request url: {url}")
            print(r)
        return r
    
    def createUrn(self,etype,ename):
        urn = f"urn:ngsi-ld:{self.user}:{etype}:{ename}"
        if self.printInfo:
            print("Fiware class. createUrn")
            print(f"urn: {urn}")  
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
            "id": self.createUrn(etype, ename),
            "type":etype,
            "name":{
                "type":"Text",
                "value":ename
                },
            "username":{
                "type":"Text",
                "value":self.user
                }
            }

        for key, value in attributes.items():
            payload[key]=value
            
        entity={
            "type":etype,
            "name":ename,
            "payload":payload
            }
        if self.printInfo:
            print("Fiware class. createEntity")
            print(json.dumps(entity, indent=4))
        
        return entity
    
    def createGeoEntity(self,etype,ename,coordinates, attributes={}):
        #coordinates=[longitude, latitude]
        
        payload={
            "id":self.createUrn(etype, ename),
            "type":etype,
            "name":{
                "type":"text",
                "value":ename
                },
            "username":{
                "type":"Text",
                "value":self.user
                },
            "location":{
                "type":"geo:json",
                "value":{
                    "type":"Point",
                    "coordinates":coordinates
                    }
                }
            }
        for key, value in attributes.items():
            payload[key]=value
        
        entity={
            "type":etype,
            "name":ename,
            "payload":payload
        }

        if self.printInfo:
            print("Fiware class. createGeoEntity")
            print(json.dumps(entity, indent=4))
        return entity
    
    def uploadEntity(self, entity):
        """
        Fijate que lo que se sube e el payload del diccionario. 
        No todo el diccionario.
        """
        self.requesResult=requests.post(
            self.urlEntities,
            headers=self.headers,
            data=json.dumps(entity["payload"])
            )
        if self.printInfo:
            print("Fiware.uploadEntity")
            fa=FiwareAnswer(answer=self.requesResult,printInfo=self.printInfo,entity=entity)
        return fa
    
    def uploadListOfEntities(self,l):
        lStatus=[]
        n=len(l)
        for i in range(len(l)):
            print(f"Uploading entity: {i} of {n}")
            fa=self.uploadEntity(l[i])
            lStatus.append(fa)
        return lStatus
    
    def filterByType(self, etype:str, limit=1000):
        self.url=self.urlEntities + "?type=" + etype + "&limit=" + str(limit)  + "&options=count"
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa 

    def filterByIdPattern(self, idSubString:str, limit=1000):
        "^.*Test.*$"
        self.url=self.urlEntities + "?idPattern=^.*" + idSubString + ".*$" + "&limit=" + str(limit)  + "&options=count"
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa

    def filterByIdPatternAndType(self, idSubString:str,etype:str, limit=1000):
        "^.*Test.*$"
        self.url=self.urlEntities + "?idPattern=^.*" + idSubString + ".*$" + "&type=" + etype +"&limit=" + str(limit)  + "&options=count"
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa

    
    def filter(self, idPattern=None, type=None, name=None, fieldsValuesDict=None, limit=1000)->FiwareAnswer:
        """
        This method gets all entities that match with all conditions.
        Makes several interation requests to get 1000 entities,
        and join them in one result.
        Parameters:
            idPattern: search in the id the text idPattern. Can be used to get all entities of a user
            etype: filter by entity type
            fieldsValuesDict: dict key:value to filter
            limit: limit of entities of each iteration
        """
        if idPattern is not None:
            parameters = {
                "idPattern": idPattern,
                "offset": 0,
            }
        else:
            parameters={}
        
        if limit is not None:
            parameters["limit"] = limit

        if type is not None:
            parameters["type"] = type

        if name is not None:
            if fieldsValuesDict is not None:
                fieldsValuesDict["name"]=name
            else:
                fieldsValuesDict={}
                fieldsValuesDict["name"]=name

        if fieldsValuesDict is not None and isinstance(fieldsValuesDict, dict):
            print(fieldsValuesDict)
            q=""
            for key, value in fieldsValuesDict.items():
                print(key,value)
                #ejemplo: q=temperature<24;humidity==75..90;status==running
                q=q+f"{key}=={value};"
                
            
            q=q[:-1]#quita el último;
            parameters["q"] = q

        if self.printInfo:
            print("Fiware.filterByUserAndProperties.Current parameters:")
            print(parameters.items())
        
        page = 0
        entities = []
        while True:
            if self.printInfo:
                print(f"Iteración: {page + 1}")
            response = requests.get(self.urlEntities, params=parameters)
            if len(response.json()) == 0:
                break
            #fa:FiwareAnswer=FiwareAnswer(answer=response,printInfo=self.printInfo)
            entities += response.json()

            if len(response.json()) <= limit:
                break
            page += 1
            parameters["offset"] = page * limit
        fa=FiwareAnswer(answer=response, printInfo=self.printInfo)
        fa.setResultingEntities(resultingEntities=entities)
        return fa

    """
    def filterByAttributeValue(self, attributeName:str, attributeValue, operator="==", limit=1000):
        #Operator can be >, ==, <
        
        self.url=self.urlEntities + "?q=" + attributeName + operator + str(attributeValue) + "&limit=" + str(limit) + "&options=count"
        self.requesResult=requests.get(self.url)
        fa:FiwareAnswer=FiwareAnswer(answer=self.requesResult)
        return fa
    """
    
    def filterBySeveralAttributeValueConditions(self, andConditions:str, limit=1000):
        """
        conditions must be like: "accuracy>2;accuracy<5;mode==8"
        Means accuracy > 2 and accuracy <5 and mode ==8
        There is not OR condition.
        """
        if self.printInfo:
            print('Fiware.filterBySeveralAttributeValueConditions')
        self.url=self.urlEntities + "?q=" + andConditions + "&limit=" + str(limit) + "&options=count"
        #self.requesResult=requests.get(self.url)
        #fa:FiwareAnswer=FiwareAnswer( answer=self.requesResult)

        page = 0
        entities = []
        offset=0
        while True:
            if self.printInfo:
                print(f"Iteración: {page + 1}")
            response = requests.get(self.url + '&offset=' + str(offset))
            if len(response.json()) == 0:
                break
            #fa:FiwareAnswer=FiwareAnswer(answer=response,printInfo=self.printInfo)
            entities += response.json()

            if len(response.json()) <= limit:
                break
            page += 1
            offset = page * limit
        
        fa=FiwareAnswer(answer=response, printInfo=self.printInfo)
        fa.setResultingEntities(resultingEntities=entities)
        #fa=FiwareAnswer(answer=response, printInfo=self.printInfo)
        #fa.setResultingEntities(resultingEntities=entities)
        #return fa

        return fa
    """
    #this does not retrieve more than 1000 entities          
    def getAllEntities(self, limit=1000):
        url=self.urlEntities + "?limit=" + str(limit) + "&options=count"
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
        if self.printInfo:
            print("Fivare.getEntityById")
        url=self.urlEntities + "/" + entity_id
        self.requesResult=requests.get(url)
        return FiwareAnswer(answer=self.requesResult)

    def countEntities(self):
        parameters={"options":"count"}
        r=requests.get(self.urlEntities,params=parameters)
        try:
            count = int(r.headers["Fiware-Total-Count"])
        except:
            count = None
        return count
    
    def deleteEntityById(self,entity_id):
        """
        There is not a feature in Fiware to delete several entities at once
        It is necessary select them and remove them one by one
        """
        url = self.urlEntities + "/" + entity_id
        if self.printInfo:
            print("Fiware.deleteEntityById")
            print(f"Deleting entity {url}")
        self.requesResult=requests.delete(url)
        fa:FiwareAnswer=FiwareAnswer(self.requesResult,printInfo=self.printInfo)
        return fa
    
    def deleteListOfEntities(self,listOfEntities:list):
        for e in listOfEntities:
            self.deleteEntityById(e['id'])

    def deleteAllEntitiesOfUser(self, username):
        if self.printInfo:
            print(f"Fiware.deleteAllEntitiesOfUser. Username: {username}")

        fa1:FiwareAnswer=self.filter(fieldsValuesDict={"username":username})
        n=len(fa1.resultingEntities)
        results:[FiwareAnswer]=[]
        for i in range(n):
            if self.printInfo:
                print(f"Deleting entity {i+1} of {n}")
            en=fa1.resultingEntities[i]
            #pay attention. Here the payload field is not
            #when you upload an entity you get the id as en["payload"]["id"]
            #but when you download an entity you simply use en["id"]
            fa:FiwareAnswer=self.deleteEntityById(en["id"])
            fa.entity=en
            results.append(fa)

    def createCsvEntities(self, etype, csvData:list, csvHeader:list, eNameFieldName:str, latLonFieldNames:list=None):
        #* csvData es is a list of lists [[1,2,...],[2,5,...]]
        #* The entity name will be the firts field values of each list,
        #   in the above example, 1, 2, ...  
        #* csv header is like: ["PID", "LONGITUDE", "LATITUDE", "ACCURACY", "DATE"]
        #ename es PID

        #data checks
        if len(csvData)==0:
            print('No data')
            return []
        nf=len(csvData[0])
        if nf ==0:#number of fiels in each reccord
            print('No data in reccords')
            return []

        csvHeaderLower=[]
        for item in csvHeader:
            csvHeaderLower.append(item.lower())

        try:
            enameIndex=csvHeaderLower.index(eNameFieldName.lower())
        except:
            print(f'{eNameFieldName} is not in the csvHeader')
            return []
        
        if latLonFieldNames is not None:
            try:
                latIndex=csvHeaderLower.index(latLonFieldNames[0].lower())
            except:
                print(f'{latLonFieldNames[0]} is not in the csvHeader')
                return []

            try:
                lonIndex=csvHeaderLower.index(latLonFieldNames[1].lower())
            except:
                print(f'{latLonFieldNames[1]} is not in the csvHeader')
                return []
        #end of data checks

        csvEntities=[]
        for record in csvData:
            attributes={}
            for index, fieldName in enumerate(csvHeader):
                value=record[index]
                if isinstance(value, float):
                    attributes[fieldName.lower()]={
                        "type": "Float",
                        "value": value
                        }
                elif isinstance(value, int):
                    attributes[fieldName.lower()]={
                        "type": "Integer",
                        "value": value
                        }
                else:
                    attributes[fieldName.lower()]={
                        "type": "Text",
                        "value": value
                        }   
            if latLonFieldNames is not None:
                entity=self.createGeoEntity(etype=etype, 
                                           ename=record[enameIndex], 
                                           coordinates=[record[latIndex],record[lonIndex]],
                                           attributes=attributes)
            else:
                entity=self.createEntity(etype=etype, 
                                           ename=record[enameIndex], 
                                           attributes=attributes)
            csvEntities.append(entity)
            if self.printInfo:
                self.printListOfDicts(csvEntities)
        return csvEntities
        
        
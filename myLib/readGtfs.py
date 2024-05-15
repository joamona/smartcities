'''
Created on 24 jul 2023

@author: joamona
'''
import os
from pickle import FALSE

class ReadGtfs(object):
    '''
    classdocs
    '''
    gtfsFolder=None
    gtfsAgency=None
    user=None
    gtfsAgency=None
    gtfsStops:[]=None

    def __init__(self, 
                 gtfsFolder='/home/joamona/www/apps/desweb/smartcities/gtfsValencia',
                 user='joamona',
                 ):
        '''
        Constructor
        '''
        self.gtfsFolder=gtfsFolder
        self.user=user
        
        self.readGtfsAgency()

    def readGtfsAgency(self):
        ### USE NGSI-LD MODEL ONLY !!!! NGSI v2 DOES NOT WORK in 2023 !!!!
        fileName=os.path.join(self.gtfsFolder, 'agency.txt')
        with open(fileName,'rt') as f:
            records=f.readlines()
        #template
        #Fiware template
        #https://smart-data-models.github.io/dataModel.UrbanMobility/GtfsAgency/examples/example-normalized.json
        payload={
          "id": None,
          "type": "GtfsAgency",
          "agencyName": {
            "type": "Property",
            "value": None
          },
          "page": {
            "type": "URL",
            "value": "http://www.emtmalaga.es/"
          },
          "timezone": {
            "type": "Text",
            "value": "Europe/Madrid"
          },
          "language": {
            "type": "Property",
            "value": "None"
          },
        }
        #agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone
        #EMT,EMT Valencia,http://www.emtvalencia.es,Europe/Madrid,es,+34963158515
        fields=records[1].strip().split(',')
        payload['id']=f'urn:nsgi-ld:{self.user}:GtfsAgency:{fields[0]}'
        payload['agencyName']['value']=fields[1]
        payload['page']['value']=fields[2]
        payload['timezone']['value']=fields[3]
        payload['language']['value']=fields[4]
        
        entity={
            'type':'GtfsAgency',
            'name':fields[1],
            'payload':payload
        }
        self.gtfsAgency=entity
        return entity
        
    def readGtfsStops(self):
        ### USE NGSI-LD MODEL ONLY !!!! NGSI v2 DOES NOT WORK in 2023 !!!!
        if self.gtfsAgency is None:
            print("You first must read de gtfsAgency")
            return
        
        filename = os.path.join(self.gtfsFolder, 'stops.txt')
        with open(filename, 'rt') as gtfs_file:
            records = gtfs_file.readlines()

        payload = {
            'id': None,
            'type': 'GtfsStop',
            'code': {'type': 'Property', 'value': None},
            'location': {
                'type': 'GeoProperty',
                'value': {'type': 'Point', 'coordinates': None}
            },
            'name': {'type': 'Property', 'value': None},
            'operatedBy': {'type': 'Relationship', 'value': None},
        }
        
        l=[]
        ### "@context" gives error 400 !!!!!
        #stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station
        #10,10,Dr. Lluch - Mare de Déu del Sufragi,C DOCTOR LLUCH 99 (DAVANT) - VALÈNCIA,39.4672336950355,-0.328305576746871,,,0,
        for record in records[1:]:#jupms the first line
            #we have to create the dictionary every iteration
            #if not we put in the list copys of the same,
            #and the last iteration modifies all the entities
            payload = {
                'id': None,
                'type': 'GtfsStop',
                'code': {'type': 'Property', 'value': None},
                'location': {
                    'type': 'GeoProperty',
                    'value': {'type': 'Point', 'coordinates': None}
                },
                'name': {'type': 'Property', 'value': None},
                'operatedBy': {'type': 'Relationship', 'value': None},
            }
            fields = record.strip().split(',')
            payload['id'] = f'urn:ngsi-ld:{self.user}:GtfsStop:{fields[0]}'
            payload['code']['value'] = fields[1]
            longitude = float(fields[5])
            latitude = float(fields[4])
            payload['location']['value']['coordinates'] = [longitude, latitude]
            payload['name']['value'] = self._forbidden(fields[2])
            payload['operatedBy']['value'] = self.gtfsAgency['payload']['id']
            entity = {
                'type': 'GtfsStop',
                'name': fields[1],
                'payload': payload
            }
            l.append(entity)
            
        self.gtfsStops=l
        return l
        
    def readGtfsShapes(self):
        pass
    
    def _forbidden(self, string):
        return string.replace('<', '[') \
                     .replace('(', '[') \
                     .replace('>', ']') \
                     .replace(')', ']') \
                     .replace('"', '-') \
                     .replace('=', '-') \
                     .replace(';', '-') \
                     .replace('\'', ' ') 

        
'''
Created on 24 jul 2023

@author: joamona
'''

from myLib.foliumMapFromFiwareEntities import FoliumMapFromFiwareEntities

#map with all gates
fm=FoliumMapFromFiwareEntities(type='Gate')
fm.openBrowser()

#map wit all user entities. If any jas no location, an alert is shown:
#   Creating map marker for entity: urn:ngsi-ld:joamona:Dummy1:K1
#   No location in entity keys
fm=FoliumMapFromFiwareEntities(fieldsValuesDict={'username':'joamona'})
fm.openBrowser()

    
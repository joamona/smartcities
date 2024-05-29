'''
Created on 4 jul 2023

@author: joamona
'''
from myLib.fiware import Fiware
upv=Fiware()
e=upv.createGeoEntity(etype='Gate3', ename='A4', 
                    coordinates=[-0.34722055,39.4831925],
                    attributes= {
                        "date": {"type": "Text","value": "2019-04-15 09:21:20"},
                        "speed": {"type": "Float","value": 225}
                    }
                )

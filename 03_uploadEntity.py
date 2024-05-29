'''
Created on 4 jul 2023

@author: joamona
'''

from myLib.fiware import Fiware
upv=Fiware()
dummy=upv.createEntity(etype='Dummy1', ename='K1', attributes={
            "accuracy": {
                "type": "Float",
                "value": 1.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        })
upv.uploadEntity(entity=dummy)

dummy=upv.createEntity(etype='Dummy2', ename='K2', attributes={
            "accuracy": {
                "type": "Float",
                "value": 2.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        })
upv.uploadEntity(entity=dummy)

dummy=upv.createEntity(etype='Dummy3', ename='K3', attributes={
            "accuracy": {
                "type": "Float",
                "value": 3.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        })
upv.uploadEntity(entity=dummy)

dummy=upv.createEntity(etype='Dummy3', ename='K4', attributes={
            "accuracy": {
                "type": "Float",
                "value": 3.0
            },
            "date": {
                "type": "Text",
                "value": "2019-04-15 09:21:20"
            }
        })
upv.uploadEntity(entity=dummy)

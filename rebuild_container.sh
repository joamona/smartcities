#!/bin/bash
docker rm fiware_orion_1
docker rm fiware_mongo_1
docker-compose up -d

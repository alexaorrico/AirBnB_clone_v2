#!/usr/bin/env bash
RED='\033[0;31m'
NC='\033[0m'
printf "${RED}test GET method to retrieve all cities from a state\n${NC}"
curl -X GET http://0.0.0.0:5000/api/v1/states/299f2b98-34a6-401e-9159-a4df728082db/cities
printf "${RED}should return a not found${NC}\n"
curl -X GET http://0.0.0.0:5000/api/v1/states/not_an_id/cities
printf "${RED} should return an object corresponding to the city id\n${NC}"
curl -X GET http://0.0.0.0:5000/api/v1/cities/598b53be-0e5f-4ea9-8baa-3bd1b6a72f47
printf "${RED} should add a new city to the corresponding state \n${NC}"
curl -X POST http://0.0.0.0:5000/api/v1/states/cb91236a-419f-4d7a-9cf9-c72af3cec8a0/cities -H "Content-Type: application/json" -d '{"name": "Los santos"}'
printf "${RED} modify the state corresponding to the given id \n${NC}"
curl -X PUT http://0.0.0.0:5000/api/v1/cities/94d457d7-f649-4522-aa69-ab6686cd3634 -H "Content-Type: application/json" -d '{"name": "Fouchena"}'
printf "${RED} delete a city by the corresponding city_id from database \n${NC}"
curl -X DELETE http://0.0.0.0:5000/api/v1/cities/598b53be-0e5f-4ea9-8baa-3bd1b6a72f47

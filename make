#!/usr/bin/bash

re=$(curl -X POST http://0.0.0.0:5050/api/v1/places_search -H "Content-Type: application/json" -d '{"states": ["421a55f4-7d82-47d9-b54c-a76916479545", "421a55f4-7d82-47d9-b54c-a76916479546"], "cities": ["521a55f4-7d82-47d9-b54c-a76916479551"]}')

echo $re | python3 -m json.tool > out.json
batcat out.json
rm out.json

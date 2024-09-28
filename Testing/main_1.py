#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5050/api/v1/amenities")
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))
    for amenity_j in r_j:
        if amenity_j.get('name') in ["Wifi", "Ethernet", "Soap", "Bed"]:
            print("OK")
        else:
            print("Missing: {}".format(amenity_j.get('name')))
        if amenity_j.get('id') is None:
            print("Missing ID for Amenity: {}".format(amenity_j.get('name')))

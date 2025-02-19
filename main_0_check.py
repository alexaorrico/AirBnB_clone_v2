#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5050/api/v1/stats")
    r_j = r.json()
    print(r_j.get("amenities", 0))
    print(r_j.get("cities", 0))
    print(r_j.get("places", 0))
    print(r_j.get("reviews", 0))
    print(r_j.get("states", 0))
    print(r_j.get("users", 0))

#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5050/api/v1/states")
    r_j = r.json()
    print(type(r_j))
    print(len(r_j))

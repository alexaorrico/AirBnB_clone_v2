#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    r = requests.get("http://0.0.0.0:5050/api/v1/status")
    print(r.json().get("status"))

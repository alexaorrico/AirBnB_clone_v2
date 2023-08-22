#!/usr/bin/python3
from models.state import State
import requests

request_get = requests.get("https://0.0.0.0:5000/api/v1/states/").to_dict()

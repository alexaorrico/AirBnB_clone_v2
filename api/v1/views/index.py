#!/usr/bin/python3
"""Doc"""
from views import app_views
import requests
import json


@app_views.route('/status')
def index():
    """ returns a JSON """
    url = app_views
    response = requests.get(url)
    
    if response.status_code == 200:
        return {'status': 'OK'}
 
#!/usr/bin/python
""" """
from api.v1.views import app_views
from json import dumps

@app_views.route('/status')
def status():
   """return succsess code 200"
    json = {"status": "OK"}
    return dumps(json)
#!/usr/bin/python3
""" Gives the status of the api """
from api.v1.views import app_views
import json


@app_views.route('/status', strict_slashes=False)
def app_status(self):
    """ Returns the status of the app in json format """
    return json.dumps({"status": "OK"})

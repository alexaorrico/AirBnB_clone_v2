#!/usr/bin/python3
""" app_view Blueprint """

from api.v1.views import app_views
import json


@app_views.route('/status', strict_slashes=False)
def show_status():
    """ Shows the api response status """
    return json.dumps({"status": 'OK'})

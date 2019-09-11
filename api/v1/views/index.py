#!/usr/bin/python3
'''Creates various routes and returns respective JSONs'''
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''Returns a JSON with status: OK'''
    return {"status": "OK"}

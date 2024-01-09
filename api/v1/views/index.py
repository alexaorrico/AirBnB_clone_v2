#!/usr/bin/python3
""" Index file for api/v1
"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    return {"status": "OK"}

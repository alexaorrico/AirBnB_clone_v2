#!/usr/bin/python3
"""accesses app_views and route /status that returns a json """

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def api_status():
    """a function that returns a json file with the api status"""

    return jsonify({"status": "OK"})

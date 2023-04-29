#!/usr/bin/python3

"""index file for flask app"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def api_status():
    """a function to return api status"""

    return jsonify({"status": "OK"})

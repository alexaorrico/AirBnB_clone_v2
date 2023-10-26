#!/usr/bin/python3
"""our index file"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)
    """
    status = {
            "status": "OK"
            }
    return jsonify(status)

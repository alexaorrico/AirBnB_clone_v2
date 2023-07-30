#!/usr/bin/python3
"""
 flask with general routes
    routes:
        /status:    display "status":"OK"
        /stats:     dispaly total for all classes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

# Define the /status route
@app_views.route('/status', strict_slashes=False)
def status():
    """return JSON of OK status """
    return jsonify({"status": "OK"})

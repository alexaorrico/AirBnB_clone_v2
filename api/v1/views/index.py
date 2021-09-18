#!/usr/bin/python3
"""Create a Index
"""
from api.v1.views import app_views
from flask import jsonify


<<<<<<< HEAD
@app_views.route("/status")
=======
@app_views.route("/status", strict_slashes=False)
>>>>>>> 09c2ab1f0098ca4fbea9572f4570ebd72ef72184
def status():
    """Returns status in jason format"""
    return jsonify({'status': 'OK'})

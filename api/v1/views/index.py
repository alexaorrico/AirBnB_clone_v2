#!/usr/bin/python3

"""
import app_views from api.v1.views
create a route /status on the object
app_views that returns a JSON: "status": "OK"
"""
from api.v1.views import app_views
from flak import jsonify


@app_views.route("/status")
def status():
    """ returns a JSON format"""
    return jsonify({"status": "OK"})

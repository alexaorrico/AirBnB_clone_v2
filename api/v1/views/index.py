#!/usr/bin/python3
import json
from flask import Response
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """status method to return status to api request"""
    return Response("{}\n".format(json.dumps({"status" : "OK"})), mimetype='application/json')

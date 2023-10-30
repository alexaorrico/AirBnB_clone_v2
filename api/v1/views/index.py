#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify

# ROUTES
@app_views.route("/status")
def status():
    """ Handles status route request """
    return jsonify({"status":"OK"})

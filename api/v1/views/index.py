#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify

@app_views.rote('/status')
def get_status():
    """returns a JSON: "status": 'OK'"""
    rep = {"status": "OK"}

    return jsonify(rep)

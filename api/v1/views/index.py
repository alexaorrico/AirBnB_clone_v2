#!/usr/bin/python3
"""basic routes for the Flask App"""
from flask import jsonify
from api.v1.views import app_views
from models import storage, classes


@app_views.route('/status')
def status_api():
    """Tests the status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects"""
    # query storage engine for each object
    objs = {}
    for key, cls in classes.items():
        # change key into lower case for returned JSON
        key = key.lower()
        # convert keys into plurals
        # yes, i was bored
        if key.endswith('y'):
            key = key.replace('y', 'ies')
        else:
            key = key + 's'
        objs[key] = storage.count(cls)
    return jsonify(objs)

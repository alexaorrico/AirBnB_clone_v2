#!/usr/bin/python3
"""Index view for the web service API"""
from flask import jsonify, make_response
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.engine.file_storage import classes


@app_views.route('/status')
def status():
    """Return API status"""
    return jsonify(status='OK')


@app_views.route('/stats')
def stats(cls=None):
    """Return number of objects by type"""

    objects = {}

    for key, value in classes.items():
        if key != 'BaseModel':
            # count objects by type from storage
            objects[key.lower()] = storage.count(value)
    return make_response(jsonify(objects))

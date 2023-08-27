#!/usr/bin/python3
""" views in app_views """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes
from models.state import State


@app_views.route('/status', strict_slashes=False)
def app_views_status():
    """ displays a status message """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ displays some stats """
    asked_classes = {
                    "amenities": storage.count(classes['Amenity']),
                    "cities": storage.count(classes['City']),
                    "places": storage.count(classes['Place']),
                    "reviews": storage.count(classes['Review']),
                    "states": storage.count(classes['State']),
                    "users": storage.count(classes['User'])
                    }
    return jsonify(asked_classes)

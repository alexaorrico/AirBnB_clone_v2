#!/usr/bin/python3
"""
Index model holds the endpoint (route)
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status/')
def status():
    """Example endpoint returns status
    returns the current status of the API
    ---
    definitions:
      status:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: dictionary with 'status' as key and 'ok' as keyvalue
        schema:
          $ref: '#/definitions/State'
        examples:
            {"status": "OK"}
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/')
def stats():
    """Example endpoint returns stats
    returns a number of objects of each class
    ---
    definitions:
      status:
        type: object
      Color:
        type: string
      items:
        $ref: '#/definitions/Color'

    responses:
      200:
        description: dictionary with 'status' as key and 'ok' as keyvalue
        schema:
          $ref: '#/definitions/State'
        examples:
           { "amenities": 47, "cities": 36, "places": 154, "reviews": 718,
             "states": 27, "users": 31}
    """
    models_available = {"User": "users",
                        "Amenity": "amenities", "City": "cities",
                        "Place": "places", "Review": "reviews",
                        "State": "states"}
    stats = {}
    for cls in models_available.keys():
        stats[models_available[cls]] = storage.count(cls)
    return jsonify(stats)

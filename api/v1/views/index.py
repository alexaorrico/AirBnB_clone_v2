#!/usr/bin/python3
"""
Creates a status and stats route that returns a JSON
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    """
    Retrieves ok status
    """
    return jsonify({"status": "OK"})


# @app_views.route('/stats', methods=['GET'], strict_slashes=False)
# def number_objects():
#     """ Gets number of each objects by type """
#     classes = [Amenity, City, Place, Review, State, User]
#     names = ["amenities", "cities", "places", "reviews", "states", "users"]

#     number_objs = {}
#     for x in range(len(classes)):
#         number_objs[names[x]] = storage.count(classes[x])

#     return jsonify(number_objs)

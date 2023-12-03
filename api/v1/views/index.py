#!/usr/bin/python3
"""
Creates a route that returns a JSON
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status_check():
    """
    Sends okay status
    """
    return jsonify({"status": "OK"})


# @app_views.route('/stats', methods=['GET'], strict_slashes=False)
# def number_objects():
#     """ Retrieves the number of each objects by type """
#     classes = [Amenity, City, Place, Review, State, User]
#     names = ["amenities", "cities", "places", "reviews", "states", "users"]

#     num_objs = {}
#     for i in range(len(classes)):
#         num_objs[names[i]] = storage.count(classes[i])

#     return jsonify(num_objs)

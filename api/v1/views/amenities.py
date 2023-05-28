#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""


import json
from models import storage
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieve_amenity():
    """
    Retreves the amenities
    """

    amenities_list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)

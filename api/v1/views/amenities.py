#!/usr/bin/python3
"""
This module handles all default RestFul API actions for Amenity objects.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def all_amenities():
    """Retrieves all Amenity objects from storage"""
    amenities = storage.all("Amenity")
    amenities_list = []
    for k, v in amenities.items():
        amenities_list.append(v.to_dict())

    return jsonify(amenities_list)

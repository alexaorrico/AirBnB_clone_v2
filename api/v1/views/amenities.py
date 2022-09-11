#!/usr/bin/python3
"""amenities register in blueprint instance"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_view('/amenities/', Methods=['GET'], strict_slashes=False)
@app_view('/amenities/<amenity_id>')
def amenity_get(amenity_id=None):
    """return all amenities objects"""
    if amenity_id is None:
        amenities = storage.all("Amenity")
        amenities_list = []
        for amenity in amenities.values():
            aminities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    else:
        storage.get("Amenity", amenity_id)


#!/usr/bin/python3
"""Creating amenity objects to handle all default RESTFUL APIs"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieving all amenities from the database"""
    amenity_list = []
    amenities = storage.all(Amenity).values()

    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
        return (jsonify(amenity_list))

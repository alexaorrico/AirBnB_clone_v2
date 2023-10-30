#!/usr/bin/python3
''' new view for amenity objects'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

#!/usr/bin/python3
"""amenitys api"""
from models.city import City
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/api/v1/amenities', methods=['GET'], strict_slashes=False)
def Amenity():
    """get all amenities"""
    content = []
    amenity = storage.get(Amenity)
    if amenity is None:
        abort(404)
    for data in amenity:
        content.append(data.to_dict())
    return jsonify(content)

@app_views.route('/api/v1/amenities/<string:amenity_id>')
def Amenity_id(amenity_id):
    verify_id = storage.get(Amenity, amenity_id)
    if verify_id is None:
        abort(404)
    return jsonify(cities.to_dict())



#!/usr/bin/python3
"""Amenity Api Module"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ """
    all_amenitys = []
    for obj in storage.all(Amenity).values():
        all_amenitys.append(obj.to_dict())
    return jsonify(all_amenitys)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def aminities_get(amenity_id):
    """ """
    if amenity_id:
        obj_amenities = storage.get(Amenity, amenity_id)
        if obj_amenities:
            return jsonify(obj_amenities.to_dict())
        abort(404)

@app_views.route('/amenities/<amenity_id', strict_slashes=False, methods=['DELETE'])
def amenities_delete(amenity_id):
    """ """
    if amenity_id:
        obj_amenities = storage.get(Amenity, amenity_id)
        if obj_amenities:
            storage.delete(obj_amenities)
            storage.save()
            return make_response(jsonify({}), 200)
        abort(404)

#!/usr/bin/python3
"""Amenities file"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():

    """list of all amenity objects"""
    list = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """list one amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return amenity.to_dict()


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Delete a amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return {}, 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def amenity_post():
    """list of all amenity objects"""

    core = request.get_json()
    if core is None:
        abort(400, description="Not a JSON")
    if 'name' not in core.keys():
        abort(400, description="Missing name")
    amenity = Amenity(**core)
    amenity.save()
    return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """list of all amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    core = request.get_json()
    if core is None:
        abort(400, description="Not a JSON")
    ignored_keys = ('id', 'created_at', 'updated_at')
    for key, value in core.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return amenity.to_dict(), 200

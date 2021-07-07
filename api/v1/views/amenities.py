#!/usr/bin/python3
"""view for Amenity objects that handles all default RestFul API actions:"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for key, value in storage.all("Amenity").items():
        amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def obj_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    kwargs = request.get_json()
    amenity = Amenity(**kwargs)
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    content = request.get_json()
    if content is None:
        abort(400, description='Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for key, val in content.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, val)
    storage.save()
    return (jsonify(amenity.to_dict()), 200)

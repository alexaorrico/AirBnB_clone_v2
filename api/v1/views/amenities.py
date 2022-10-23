#!/usr/bin/python3

"""Module to handle amenities request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """return json array of all amenities"""
    amenities = storage.all(Amenity).values()
    return jsonify([val.to_dict() for val in amenities])


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**body)
    new_amenity.save()
    if storage.get(Amenity, new_amenity.id) is not None:
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Method to get an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(state_id):
    """update properties of a single amenity"""
    amenity = storage.get(Amenity, state_id)
    if amenity is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(amenity, k, v)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)

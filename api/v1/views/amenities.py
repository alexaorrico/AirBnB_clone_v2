#!/usr/bin/python3
'''Contains the Amenity view for the API.'''
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities_list = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in amenities_list.values()])


@app_views.route('/amenities/<amenities_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenities_id):
    """Retrieves a Amenity object"""
    state = storage.get(Amenity, amenities_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/amenities/<amenities_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenities_id):
    """Deletes a Amenity object"""
    state = storage.get(Amenity, amenities_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    obj = Amenity(**request.get_json())
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenities_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenities_id):
    """Updates a Amenity object"""
    obj = storage.get(Amenity, amenities_id)
    if obj is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)

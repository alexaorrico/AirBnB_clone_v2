#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def get_amenities():
    """Retrieves the list of all Amenity objects """
    amenities_list = [
        amn.to_dict()
        for amn in storage.all(Amenity).values()
    ]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """Retrieves a amenity object based onstate_id, raises a 404 error
    if amenity_id is not linked to any Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a amenity Object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def add_amenity():
    """creates a amenity"""
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    if 'name' not in request.get_json():
        return ("Missing name\n", 400)
    request_data = request.get_json()
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json(force=True, silent=True):
        return ("Not a JSON\n", 400)
    request_data = request.get_json()
    request_data.pop('id', None)
    request_data.pop('created_at', None)
    request_data.pop('updated_at', None)
    for key in request_data:
        setattr(amenity, key, request_data[key])
    amenity.save()
    return jsonify(amenity.to_dict()), 200

#!/usr/bin/python3
"""Module to create a new view for State objects"""
from flask import jsonify, Flask, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenities objects"""
    all_amenities = storage.all('Amenity')
    my_list = []
    for value in all_amenities.values():
        my_list.append(value.to_dict())
    return (jsonify(my_list))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves the amenity by ID"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes an amenity by ID"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Post a Amenity object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Put an Amenity instance"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))

    # TODO
    # Ignore id, created_at and updated_at
    for k, v in data.items():
        setattr(amenity, k, v)
        storage.new(amenity)
        storage.save()
    return jsonify(amenity.to_dict()), 200

#!/usr/bin/python3
""" This module handles all default RESTFUL api actions for Amenity objects"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def all_amenity():
    """ Retrieves list of all Amenity objects """
    amenity_lists = []
    for objects in storage.all(Amenity).values():
        amenity_objects = objects.to_dict()
        amenity_lists.append(amenity_objects)
    return jsonify(amenity_lists)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_single_amenity(amenity_id):
    """ Retrieves a single state based on state id"""
    for amenity_object in storage.all(Amenity).values():
        objects = amenity_object.to_dict()
        if amenity_id == objects['id']:
            return objects
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_object(amenity_id):
    """ Deletes a state object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity_object():
    """ Creates a State """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(name=data['name'])
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity_object(amenity_id):
    """ Updates a State object """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

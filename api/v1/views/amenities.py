#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amen():
    """gets all state objects"""
    all_objects = storage.all(Amenity)
    single_object = []
    for all_objects in all_objects.values():
        single_object.append(all_objects.to_dict())
    return jsonify(single_object)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amen_id(amenity_id):
    """gets the state object using his id"""
    all_objects = storage.all(Amenity)
    new_dict = {}
    for key, value in all_objects.items():
        if amenity_id == value.id:
            new_dict = value.to_dict()
            return jsonify(new_dict)
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amen(amenity_id=None):
    """Deletes"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amen():
    """Creates"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    if 'name' not in res:
        abort(400, {"Missing name"})
    obj = Amenity(name=res['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amen(amenity_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

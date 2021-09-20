#!/usr/bin/python3
"""creates a new view for State Objects"""
from models.place import Place
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places():
    """gets all state objects"""
    all_objects = storage.all(Place)
    single_object = []
    for all_objects in all_objects.values():
        single_object.append(all_objects.to_dict())
    return jsonify(single_object)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place():
    """Creates a new place"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    if 'name' not in res:
        abort(400, {"Missing name"})
    obj = State(name=res['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """gets the state object using his id"""
    all_objects = storage.all(Place)
    new_dict = {}
    for key, value in all_objects.items():
        if place_id == value.id:
            new_dict = value.to_dict
            return jsonify(new_dict)
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Deletes"""
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

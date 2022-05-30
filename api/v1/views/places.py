#!/usr/bin/python3
"""
State objects that handles all default RestFul API actions
"""

from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all places in a city objects
    """
    city = storage.get('City', city_id)
    places_list = []
    if city:
        for value in city.places:
            places_list.append(value.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    """
    if storage.get('Place', place_id):
        return jsonify(storage.get('Place', place_id).to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete a State object
    """
    if storage.get('Place', place_id):
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places/", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create a Place object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    if 'name' not in request.json:
        abort(400, "Missing name")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    user_id = request.get_json().get("user_id")
    if storage.get("User", user_id) is None:
        abort(404)
    obj_place = Place(**request.get_json())
    obj_place.city_id = city_id
    storage.save()
    _status = jsonify(obj_place.to_dict())
    _status.status_code = 201
    return _status


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Delete a State object
    """
    if not request.is_json:
        abort(400, "Not a JSON")
    obj_place = storage.get('Place', place_id)
    if obj_place:
        _data = request.get_json()
        if type(_data) is dict:
            ls_to_avoid = ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']
            for name, value in _data.items():
                if name not in ls_to_avoid:
                    setattr(obj_place, name, value)
            storage.save()
            return jsonify(obj_place.to_dict())
    abort(404)

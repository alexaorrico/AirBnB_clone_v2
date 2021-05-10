#!/usr/bin/python3
"""Handles all default Restful actions for Places"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import request, abort, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_all_places(city_id):
    """lists all places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    places = []
    for place in storage.all("Place").values():
        places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """Retrieves a given placed based on place id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id=None):
    """Deletes a place"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    else:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places(city_id):
    """Creates a place"""
    req_dict = request.get_json(silent=True)
    if req_dict is None:
        abort(400, "Not a JSON")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if "user_id" not in req_dict:
        abort(400, "Missing user_id")
    user = storage.get("User", req_dict.get("user_id"))
    if user is None:
        abort(404)
    if "name" not in req_dict.keys():
        abort(400, "Missing name")

    req_dict["city_id"] = city_id
    new_place = Place(**req_dict)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id=None):
    """Updates a place object"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)

    req_dict = request.get_json(silent=True)
    if req_dict is None:
        abort(400, "Not a JSON")
    else:
        for key, value in req_dict.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place_obj, key, value)
        storage.save()
        return jsonify(place_obj.to_dict()), 200

#!/usr/bin/python3
"""Place objects that handles all default RESTFul API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 method=['GET'], strict_slashes=False)
def get_all_place(city_id=None):
    """get lists of the place object of the give city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place = storage.all("Place")
    city_list = []
    for value in place.values():
        if value.city_id == city_id:
            city_list.append(value.to_dict())
    return jsonify(city_list)


@app_views.route('/places/<place_id>', method=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """return each place objects which give place_id"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    obj = obj.to_dict()
    return jsonify(obj)


@app_views.route('/places/<place_id>', method=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """delete each place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', method=['POST'], strict_slashes=False)
def create_place(city_id=None):
    """create a new place"""
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in args:
        return jsonify({"error": "Missing user_id"}), 400
    elif "name" not in args:
        return jsonify({"error": "Missing name"}), 400
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    user_id = args["user_id"]
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    args["city_id"] = city_id
    obj = Place(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', method=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Update each place"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    args = request.get_json()
    if args is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in args.items():
        if key not in ["id", "city_id", "user_id", "update_at", "created_at"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

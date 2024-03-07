#!/usr/bin/python3
"""
View for `Place` object that handles all default RESTFul API actions.
"""
from models import storage
from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views, City, Place


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_place_objects(city_id):
    """returns: list of all places"""
    place_list = []
    places = storage.all(Place)
    for place in places.values():
        if place.city_id == city_id:
            place_list.append(place)
    return place_list
    # city_id is not linked to City object
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place_object(place_id):
    """returns: a place object of specified id"""
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    # object not found
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_object(place_id):
    """delete: a place object"""
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    # object not found
    abort(404)


@app_views.route("/cities/city_id/places", methods=["POST"],
                 strict_slashes=False)
def create_place_object():
    """create: a place object"""
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = getattr(data, 'user_id')
    users = storage.all(User)
    for user in users.values():
        if user.id == user_id:
            new_place = Place(**data)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
    # user_id not linked to any user object
    abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place_object(place_id):
    """update: a place obect"""
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            # update place object
            for k, v in data.items():
                if k == 'id' or k == 'user_id' or k == 'city_id'\
                or k == 'created_at' or k == 'updated_at':
                    continue
                setattr(place, k, v)
                storage.save()
            return jsonify(place.to_dict()), 200
    # object not found
    abort(404)

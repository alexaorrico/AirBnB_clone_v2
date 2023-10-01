#!/usr/bin/python3
"""module to handle requests regarding a Place object"""

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_city_place(city_id):
    """retrieves list of all Place objs of a City"""
    response = storage.get(City, city_id)
    if response is None:
        # CHECK THIS, FAILS BUT RETURNS A STATUS CODE OF 200
        abort(404)

    all_places = storage.all(Place)
    list_places = []
    for key, value in all_places.items():
        if city_id == value.city_id:
            list_places.append(value.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def server_place_id(place_id):
    """Retrives a State object"""
    # check if the place id exists for a Place obj
    response = storage.get(Place, place_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_obj(place_id):
    """deletes a State object"""
    place_to_delete = storage.get(Place, place_id)

    if place_to_delete is None:
        abort(404)

    storage.delete(place_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_new_place(city_id):
    """creates a Place object"""

    response = storage.get(City, city_id)

    if response is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    # if name not in dict
    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    if data_entered.get('user_id') is None:
        abort(400, description="Missing user_id")

    # check if the entered user_id is not linked to any User object
    user_id_response = storage.get(User, data_entered.get('user_id'))
    if user_id_response is None:
        abort(404)

    new_place = Place(**data_entered)
    setattr(new_place, "city_id", city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_obj(place_id):
    """updates a State object"""
    place_to_update = storage.get(Place, place_id)

    if place_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_to_update, key, value)

    storage.save()

    return jsonify(place_to_update.to_dict()), 200

#!/usr/bin/python3
'''
Handles all default RESTFul API actions for User objects
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City

F = False


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=F)
def get_place_objs(city_id):
    '''handles Get for all place objects for a city'''

    place_list = []
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    place_objs = storage.all(Place)
    for obj in place_objs.values():
        if obj.city_id == city_id:
            place_list.append(obj.to_dict())

    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=F)
def get_place_obj(place_id):
    '''handles Get for a place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    place_dict = place_obj.to_dict()
    return jsonify(place_dict)


@app_views.route('/place/<place_id>', methods=['DELETE'], strict_slashes=F)
def delete_place_obj(place_id):
    '''deletes a place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_obj(city_id):
    '''creates place objects'''

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in json_data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'name' not in json_data.keys():
        return jsonify({"error": "Missing name"}), 400

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)

    new_obj = Place()
    for attr, val in json_data.items():
        setattr(new_obj, attr, val)
    # new_obj = State(**json_data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=F)
def update_user_obj(place_id):
    '''updates a place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for attr, val in json_data.items():
        if attr not in ("id", "user_id", "created_at", "updated_at"):
            setattr(user_obj, attr, val)
    state_obj.save()

    return jsonify(place__obj.to_dict()), 200

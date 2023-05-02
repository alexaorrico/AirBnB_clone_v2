#!/usr/bin/python3
'''
Handles all default RESTFul API actions for Place objects
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'], strict_slashes=False)
def get_places(city_id):
    '''retrieves the list of all Place objects of a City'''

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    places_list = [
        place.to_dict() for place in city_obj.places]
    return jsonify(places_list)


@app_views.route(
        '/places/<place_id>',
        methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''retrieves a Place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    '''deletes a Place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'], strict_slashes=False)
def create_place(city_id):
    '''creates a Place object'''

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'user_id' not in json_data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    elif 'name' not in json_data.keys():
        return jsonify({"error": "Missing name"}), 400

    user_obj = storage.get(User, json_data['user_id'])
    if user_obj is None:
        abort(404)

    json_data['city_id'] = city_id
    new_obj = Place(**json_data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route(
        '/places/<place_id>',
        methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''updates a Place object'''

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for attr, val in json_data.items():
        if attr not in [
                'id', 'user_id', 'city_id',
                'created_at', 'updated_at']:
            setattr(place_obj, attr, val)

    place_obj.save()

    return jsonify(place_obj.to_dict()), 200

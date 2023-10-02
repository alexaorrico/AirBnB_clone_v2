#!/usr/bin/python3
"""
This Module contains Place objects that
handles all default RESTFul API actions
"""
from flask import request, abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    places = city.places
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place based on its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a place ob based on its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """create a place for a particular ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(400)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')

    required_keys = ['user_id', 'name']
    if required_keys[0] not in json_request:
        abort(400, 'Missing user_id')
    if storage.get(User, json_request['user_id']) is None:
        abort(404)
    if required_keys[1] not in json_request:
        abort(400, 'Missing name')
    place = Place(city_id=city_id, **json_request)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updated a place attributes based on its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in json_request.items():
        if key is not ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

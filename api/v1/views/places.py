#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.city import City
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """ Returns all places from state id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_individual_place(place_id):
    """" Returns indivuidual cities by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes individual by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    """ Delete the place """
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a new city by using the URL """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, 'Not a JSON')
    user_id = my_dict.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    name = my_dict.get('name')
    if name is None:
        abort(400, 'Missing name')
        place = Place(name=name, user_id=user_id, city_id=city_id)
    for key, value in my_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a city by City ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, 'Not a JSON')
    for key, value in my_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

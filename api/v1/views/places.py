#!/usr/bin/python3
"""handles all default RESTFul API actions"""
import re
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import city
from models import place
from models.place import Place
from models.city import City
from models.user import User
from models.state import State



@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id=None):
    """liste all cities of a state"""
    list_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for  place in city.places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """get one place"""
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """ Delete a place"""
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def add_place(city_id=None):
    """add a place to a city"""
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    if city_id is None:
        abort(404)
    if 'user_id' not in requeste:
        abort(400, "Missing user_id")
    if 'name' not in requeste:
        abort(400, "Missing name")

    city = storage.get(City, city_id)
    user = storage.get(User, requeste['user_id'])
    if city and user is None:
        abort(404)

    new_place = Place(**requeste)
    new_place.city_id = city.id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


'''
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """update a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    for key, value in requeste.items():
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

'''

#!/usr/bin/python3
'''BLueprint implementation for city model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import os


@app_views.route('places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_places(place_id=None):
    '''Return the list of all City objects'''
    if request.method == 'DELETE':
        return del_place(place_id)
    elif request.method == 'PUT':
        return update_place(place_id)
    elif request.method == 'GET':
        return get_place(place_id)


@app_views.route('cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    '''Hadnles direction to actual view function'''
    if request.method == 'POST':
        return add_place(city_id)
    elif request.method == 'GET':
        return get_city_place(city_id)


def get_city_place(city_id):
    '''Return all citie linked to a city'''
    print(city_id)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


def get_place(place_id):
    '''Reurn a city given an id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


def del_place(place_id):
    '''Deletes a place obj with place_id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


def add_place(city_id):
    '''Adds city to cities'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_data:
        abort(400, 'Missing user_id')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    user = storage.get(User, req_data['user_id'])
    if not user:
        abort(404)
    place = Place(**req_data)
    place.city_id = city_id
    place.save()
    return get_place(place.id), 201


def update_place(place_id):
    '''Update a city instance'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    for key, val in req_data.items():
        skip = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
        if key not in skip:
            setattr(place, key, val)
    place.save()
    return get_place(place.id), 200

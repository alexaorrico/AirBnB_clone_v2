#!/usr/bin/python3
"""places"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


def get_city_obj(city_id):
    '''Retrieve city object by id'''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return city


@app_views.route('/cities/<city_id>/places')
def list_places_of_city(city_id):
    '''Retrieve list of all Place objects in a city'''
    city = get_city_obj(city_id)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    '''Retrieve a Place object by id'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Delete a Place object by id'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Create a new Place'''
    city = get_city_obj(city_id)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    user_id = data['user_id']
    if not storage.get("User", user_id):
        abort(404)

    new_place = Place(name=data['name'], user_id=user_id, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    '''Update a Place object by id'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key in ['name', 'description', 'number_rooms', 'number_bathrooms',
                'max_guest', 'price_by_night', 'latitude', 'longitude']:
        if key in data:
            setattr(place, key, data[key])

    storage.save()
    return jsonify(place.to_dict()), 200
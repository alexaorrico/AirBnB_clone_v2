#!/usr/bin/python3
"""
New view for Place objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/api/v1/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ retrieve list of all Place objects """
    all_places = []
    if not storage.get('City', city_id):
        abort(404)
    for place in storage.all('Place').values():
        if city_id == place.to_dict()['city_id']:
            all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/api/v1/places/<place_id>', strict_slashes=False)
def retrieve_place(place_id):
    """ retrieve a particular Place """
    place = storage.get('Place', place_id)
    if place:
        return place.to_dict()
    abort(404)


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete a Place """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return {}
    abort(404)


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create a Place """
    place_name = request.get_json()
    if not storage.get('City', city_id):
        abort(404)
    if not place_name:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in place_name:
        abort(400, {'Missing user_id'})
    elif not storage.get('User', place_name['user_id']):
        abort(404)
    elif 'name' not in place_name:
        abort(400, {'Missing name'})
    place_name['city_id'] = city_id
    new_place = Place(**place_name)
    storage.new(new_place)
    storage.save()
    return new_place.to_dict(), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ update a Place """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_place = storage.get('Place', place_id)
    if not my_place:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(my_place, key, value)
    storage.save()
    return my_place.to_dict()

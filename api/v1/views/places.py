#!/usr/bin/python3
'''
Module: 'places'
'''

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False
        )
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    return jsonify([place.to_dict() for place in City.get(city_id).places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    return jsonify(Place.get(place_id).to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place(place_id):
    """ Deletes a Place object """
    Place.get(place_id).delete()
    storage.save()
    return jsonify({})


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
        )
def create_place(city_id):
    """ Creates a Place """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    place = Place(**request.json)
    setattr(place, 'city_id', city.id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())

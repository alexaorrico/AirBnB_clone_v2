#!/usr/bin/python3
"""
Methods for Place class in our API
"""
from models.city import City
from models.place import Place
from models import storage
import json
from flask import Flask, jsonify, request, make_response, abort
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                strict_slashes=False)
def get_place_by_city(city_id):
    """Method to get al cities by city id"""
    cities = storage.all(City)
    places = storage.all(Place)
    places_in_city = []
    for city in cities.values():
        if city.id == city_id:
            for city in cities.values():
                if place.city_id == city_id:
                    places_in_city.append(place.to_dict())
            return jsonify(places_in_city)
    abort(404)
    return


@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Get a single place by id number"""
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            return(jsonify(place.todict()))
    abort(404)
    return


@app_views.route('place/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a single place"""
    places = storage.all(Place)

    for place in place.values():
        if place.id == place_id:
            place.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)

    
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place"""
    payload = request.get_json(silent=True)
    cities = storage.all(City)

    if payload is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in payload:
        abort(400, 'Missing user_id')
    elif 'name' not in payload:
        abort(400, 'Missing name')

    for city in cities.values():
        if city.id == city_id:
            new_place = Place(**payload)
            new_place.save()
            return(jsonify(new_place.to_dict()), 201)
    abort(404)
    return


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Method to update a place object"""
    payload = request.get_json(silent=True)
    places = storage.all(Place)

    if payload is None:
        abort(400, 'Not a JSON')

    for place in cities.values():
        if place.id == place_id:
            for k, v in payload.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id'\
                   and k !='user_id' and k != 'city_id':
                    setattr(place, k, v)
            place.save()
            return(jsonify(place.to_dict()), 200)
    abort(404)

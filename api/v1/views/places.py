#!/usr/bin/python3
"""New Funtion places"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET\
'], strict_slashes=False)
def displayPlacesByCity(city_id):
    """Return the places by city if not error 404
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    lista = []
    for i in city.places:
        lista.append(i.to_dict())
    return jsonify(lista)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def displayPlacesbyId(place_id):
    """Return the places by id if not error 404
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE\
'], strict_slashes=False)
def deletePlace(place_id):
    """Delete a place if not error 404
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST\
'], strict_slashes=False)
def createPlace(city_id):
    """Create a place for a city if not error 404
    """
    cities = storage.get('City', city_id)
    if not cities:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place.keys():
        abort(400, {'Missing user_id'})
    userid = storage.get('User', place['user_id'])
    if not userid:
        abort(404)
    if 'name' not in place:
        abort(400, {'Missing name'})
    new_place = Place(**place)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Update a place if not error 404
    """
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    places = storage.get('Place', place_id)
    if not places:
        abort(404)

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place.items():
        if key not in ignore:
            setattr(places, key, value)
    storage.save()
    return make_response(jsonify(places.to_dict()), 200)

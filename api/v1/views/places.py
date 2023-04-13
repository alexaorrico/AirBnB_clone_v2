#!/usr/bin/python3
'''
    Place route for the API
'''
from flask import Flask
from models import storage
from models.place import Place
from models.city import City
from models.user import User

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id):
    """get place information for all places"""
    places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_places_by_id(place_id):
    """get place information for specific places"""
    place = storage.get(Place, place_id)
    if place != None:
        return jsonify(place.to_dict())
    else:
        abort(404)

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ create a place"""
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if not 'name' in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if not 'user_id' in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    createJson['city_id'] = city_id
    user = storage.get(User, createJson['user_id'])
    if user is None:
        abort(404)
    place = Place(**createJson)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr is not 'id' or attr is not 'created_at' or attr is not 'updated_at' or attr is not 'user_id' or attr is not 'city_id':
            setattr(place, attr, val)
    storage.save()
    return jsonify(place.to_dict())

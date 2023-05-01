#!/usr/bin/python3

'''
This module creates a new view for the places objects
Routes:
    GET /api/v1/cities/<city_id>/places - Returns all places
    GET /api/v1/places/<place_id> - Returns a place object
    DELETE /api/v1/places/<place_id> - Deletes a place object
    POST /api/v1/cities/<city_id>/places - Creates a place
    PUT /api/v1/places/<place_id> - Updates a place object
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''Retrieves all places in a city'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''
    Retrieves a place object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
    Deletes a place object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
    Creates a new place object
    '''
    city = storage.get(City, city_id)
    body = request.get_json()
    if city is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in body:
        abort(400, 'Missing user_id')
    if 'name' not in body:
        abort(400, 'Missing name')
    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)
    body['city_id'] = city_id
    place = Place(**body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    Updates a place object
    '''
    place = storage.get(Place, place_id)
    body = request.get_json()
    if place is None:
        abort(404)
    if body is None:
        abort(400, 'Not a JSON')
    for k, v in body.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200

#!/usr/bin/python3
'''places.py'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id=None):
    '''get places by city'''
    city = storage.get(City, city_id)
    if city:
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    '''get place'''
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    '''delete place'''
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    '''post place'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    city = storage.get(City, city_id)
    if city:
        place = Place(**request.get_json())
        place.city_id = city.id
        place.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    '''UPdate place'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if place:
        (request.get_json()).pop('id', None)
        (request.get_json()).pop('updated_at', None)
        (request.get_json()).pop('created_at', None)
        (request.get_json()).pop('city_id', None)
        (request.get_json()).pop('user_id', None)
        for key, value in request.get_json().items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    else:
        abort(404)

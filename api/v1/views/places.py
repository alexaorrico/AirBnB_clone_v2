#!/usr/bin/python3
'''
Methods and routes for working with place data
'''
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    '''
    Gets all places
    '''
    all_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all('City').values()
    for place in places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods-['GET'], strict_slashes=False)
def retrieve_city(place_id):
    '''
    gets 1 place object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    '''
    Deletes a place object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return ({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def make_place(city_id):
    '''
    creates a place object
    '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_name = request.get_json()
    if place_name is None:
        abort(400, 'not a JSON')
    if 'user_id' not in place_name:
        abort(400, 'Missing user_id')
    if 'user_id' not in User:
        abort(404)
    if 'name' not in place_name:
        abort(400, 'Missing Name')
    place = Place(**place_name)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    update a place object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_name = request.get_json()
    if not request.get_json():
        abort(400, 'not a JSON')
    for key, value in place_name.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(place, key, value)
    storage.save()
    all_places = place.to_dict()
    return jsonify(all_places), 200

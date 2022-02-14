#!/usr/bin/python3
"""places routes"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from flasgger.utils import swag_from


@app_views.route('/cities/<string:city_id>/places', strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def city_places(city_id):
    """list all places by city"""
    city = storage.get('City', city_id)
    print(city)
    if city is None:
        abort(404, 'Not found')
    places = [obj.to_dict() for obj in (storage.all('Place')).values()
              if obj.city_id == city_id]
    return jsonify(places), 200


@app_views.route('/places/<string:place_id>', strict_slashes=False)
def get_place(place_id):
    """json data of a single place"""
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete data of a single place"""
    place = storage.get('Place', place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404, 'Not found')


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a new place"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if dictionary.get('user_id') is None:
        abort(400, 'Missing user_id')
    user = storage.get('User', dictionary.get('user_id'))
    if user is None:
        abort(404)
    if dictionary.get('name') is None:
        abort(400, 'Missing name')
    dictionary['city_id'] = city_id
    place = Place(**dictionary)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update data of place"""
    dictionary = request.get_json()
    if dictionary is None:
        abort(400, 'Not a JSON')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    [setattr(place, key, value) for key, value in dictionary.items()
     if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']]
    place.save()
    return jsonify(place.to_dict()), 200

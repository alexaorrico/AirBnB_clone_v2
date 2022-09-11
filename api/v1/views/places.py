#!/usr/bin/python3
"""register places in blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False
        )
def places_bycity(city_id=None):
    """return places of a city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    list_places = []
    for place in city.places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_byid(place_id=None):
    """return place by id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def places_delete(place_id=None):
    """delete place by id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
        )
def places_post(city_id=None):
    """add new place"""
    response = request.get_json()
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if response is None:
        abort(400, description='Not a JSON')
    if 'user_id' not in response.keys():
        abort(400, 'Missing user_id')
    user = storage.get('User', response['user_id'])
    if user is None:
        abort(404)
    if 'name' not in response.keys():
        abort(400, 'Missing name')
    response['city_id'] = city_id
    new_place = Place(**response)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def places_put(place_id=None):
    """update places obj"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, description='Not a JSON')
    response.pop('id', None)
    response.pop('user_id', None)
    response.pop('city_id', None)
    response.pop('created_at', None)
    response.pop('updated_at', None)
    for key, value in response.items():
        setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

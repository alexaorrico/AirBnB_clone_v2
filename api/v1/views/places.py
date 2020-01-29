#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_cities_id(city_id):
    """ Return the places related to a state id """
    catch_city = storage.get('City', city_id)
    match_places = storage.all('Place')
    if catch_city is None:
        abort(404)
    places_list = []
    for place in match_places.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """ Return the place form a id """
    catch_place = storage.get('Place', pace_id)
    if catch_place is None:
        abort(404)
    return jsonify(catch_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place_id(place_id):
    """ Delete the place form a id """
    catch_place = storage.get('Place', place_id)
    if catch_place is None:
        abort(404)
    storage.delete(catch_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """ Return places associated with a city id """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    catch_city = storage.get('City', city_id)
    catch_user = storage.get('User', data['user_id'])
    if catch_city is None or catch_user is None:
        abort(404)
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_places_id(place_id):
    """ Update a place from a id passed"""
    catch_place = storage.get('Place', place_id)
    if catch_place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if not key in ['user_id', 'city_id', 'id', 'created_at', 'updated_at']:
            setattr(catch_place, key, value)
    storage.save()
    return jsonify(catch_place.to_dict()), 200

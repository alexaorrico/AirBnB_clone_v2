#!/usr/bin/python3
"""
    Handles API functions for Place
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """
        Handles places in a specified city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'user_id' not in info:
            abort(400, 'Missing user_id')
        user = storage.get(User, info['user_id'])
        if user is None:
            abort(404)
        if 'name' not in info:
            abort(400, 'Missing name')
        info['city_id'] = city_id
        new_place = Place(**info)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_object(place_id):
    """
    Handles a specified Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        for review in place.reviews:
            storage.delete(review)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """
        Searching for a place using filters: State, City & Amenity
    """
    info = request.get_json(silent=True)
    if info is None:
        abort(400, 'Not a JSON')

    places = storage.all(Place)
    place_list = []

    count = 0
    for key in info.keys():
        if len(info[key]) > 0 and key in ['states', 'cities', 'amenities']:
            count = 1
            break
    if len(info) == 0 or count == 0 or not info:
        for place in places.values():
            place_list.append(place.to_dict())
        return jsonify(place_list)

    if 'amenities' in info and len(info['amenities']) > 0:
        for a_id in info['amenities']:
            for place in places.values():
                if storage_t == 'db':
                    for amenity in place.amenities:
                        if amenity.id == a_id:
                            place_list.append(place)
                            break
                elif a_id in place.amenity_ids:
                    place_list.append(place)
    else:
        for place in places.values():
            place_list.append(place)

    if 'cities' in info and len(info['cities']) > 0:
        tmp = []
        for c_id in info['cities']:
            for place in place_list:
                if place.city_id == c_id:
                    tmp.append(place)
        if 'states' in info and len(info['states']) > 0:
            for s_id in info['states']:
                state = storage.get(State, s_id)
                for city in state.cities:
                    if city.id in info['cities']:
                        count = 2
                        break
                if count == 2:
                    continue
                for place in place_list:
                    city_id = place.city_id
                    city = storage.get(City, city_id)
                    if city.state_id == s_id and place not in tmp:
                        tmp.append(place)
        place_list = tmp
    elif 'states' in info and len(info['states']) > 0:
        tmp = []
        for s_id in info['states']:
            for place in place_list:
                city_id = place.city_id
                city = storage.get(City, city_id)
                if city.state_id == s_id:
                    tmp.append(place)
        place_list = tmp

    tmp = []
    for place in place_list:
        result = place.to_dict()
        if 'amenities' in result:
            del result['amenities']
        tmp.append(result)
    return jsonify(tmp)

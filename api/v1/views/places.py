#!/usr/bin/python3
"""Module with the view for Place objects"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models import storage
from flask import request, abort, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Return a list of dictionaries of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = []
        for city in city.places:
            places.append(city.to_dict())
        return jsonify(places)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'user_id' not in data.keys():
        return 'Missing user_id', 400
    user = storage.get(User, data.get('user_id'))
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        return 'Missing name', 400
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place(place_id):
    """Get a place instance from the storage"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'city_id' or k != 'user_id'\
               or k != 'created_at' or k != 'updated_at':
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search in places"""
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    states = []
    cities = []
    places = []
    if 'states' in data.keys():
        for state_id in data['states']:
            states.append(storage.get(State, state_id))
        for state in states:
            for city in state.cities:
                cities.append(city)
    if 'cities' in data.keys():
        for city_id in data['cities']:
            new_city = storage.get(City, city_id)
            if new_city not in cities:
                cities.append(new_city)
    if cities == [] and\
       ('amenities' not in data.keys() or data['amenities'] == []):
        for place in storage.all(Place).values():
            places.append(place.to_dict())
        return jsonify(places)
    if cities == []:
        for place in storage.all(Place).values():
            places.append(place)
    if 'amenities' not in data.keys() or data['amenities'] == []:
        for city in cities:
            for place in city.places:
                places.append(place.to_dict())
        return jsonify(places)
    else:
        if places == []:
            for city in cities:
                for place in city.places:
                    check = 0
                    for amenity_id in data['amenities']:
                        new_amenity = storage.get(Amenity, amenity_id)
                        if new_amenity and new_amenity not in place.amenities:
                            check = 1
                            break
                    if check == 0:
                        place = place.to_dict()
                        del place['amenities']
                        places.append(place)
            return jsonify(places)
        else:
            places_amenities = []
            for place in places:
                check = 0
                for amenity_id in data['amenities']:
                    new_amenity = storage.get(Amenity, amenity_id)
                    if new_amenity and new_amenity not in place.amenities:
                        check = 1
                        break
                if check == 0:
                    place = place.to_dict()
                    del place['amenities']
                    places_amenities.append(place)
            return jsonify(places_amenities)

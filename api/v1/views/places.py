#!/usr/bin/python3
""" Endpoints for place related
    interactions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def place_by_city(city_id):
    """search for a city with given id and:
       return all list of its places
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        if 'user_id' not in data.keys():
            return make_response('Missing user_id\n', 400)
        if 'name' not in data.keys():
            return make_response('Missing name\n', 400)
        if storage.get(User, data.get('user_id')) is None:
            abort(404)
        data.update({'city_id': city_id})
        new_place = Place(**data)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def place_by_id(place_id):
    """search for a place with given id and:
        1. return it
        2. update it
        3. delete it
       depending on the method
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        data = get_json(request)
        if not data:
            return make_response('Not a JSON\n', 400)
        for key, value in data.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', strict_slashes=False,
                 methods=['POST'])
def place_search():
    """search places using JSON
       data passed in the request
       body:
       inclusive filters
        1. states
        2. cities
       exclusive filters
        1. amenities
    """
    filters = get_json(request)
    if filters is None:
        return make_response('Not a JSON\n', 400)

    places = []
    if "states" in filters.keys():
        states = [storage.get(State, state_id)
                  for state_id in filters.get('states')]
        for state in states:
            for city in state.cities:
                create_place_list(places, city, filters.get('amenities'))
    if "cities" in filters.keys():
        cities = [storage.get(City, city_id)
                  for city_id in filters.get('cities')]
        for city in cities:
            create_place_list(places, city, filters.get('amenities'))
    if len(filters) == 0 or all([len(filters) == 1,
                                filters.get('amenities') is not None]):
        states = storage.all(State).values()
        for state in states:
            for city in state.cities:
                create_place_list(places, city, filters.get('amenities'))

    return make_response(jsonify(places))


def create_place_list(place_list, city, amenities=None):
    """ create a list of places based on specified amenities
    """
    if amenities is not None:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in amenities]
        for place in city.places:
            place_dict = place.to_dict()

            #  for db storage: query place.amenities
            #  add attributes amenites with list of
            #  unserializable amenities objects
            #  the key-value pair must be removed
            #  to prevent JSON serializaiton errors.
            #  This also ensures consistency in the
            #  object string representation
            if place_dict.get("amenities"):
                place_dict.pop("amenities")
            if all([amenity in place.amenities for amenity in amenities]):
                if place_dict not in place_list:
                    place_list.append(place_dict)
    else:
        for place in city.places:
            place_dict = place.to_dict()
            if place_dict.get("amenities"):
                place_dict.pop("amenities")
            if place.to_dict() not in place_list:
                place_list.append(place_dict)


def get_json(request):
    """check if body has json data
       and handles errors reponses
    """
    #  exception handling to avoid calling
    #  on_json_loading_failed()
    try:
        data = request.get_json()
    except Exception:
        data = None
    return data

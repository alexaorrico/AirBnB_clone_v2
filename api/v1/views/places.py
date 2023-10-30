#!/usr/bin/python3
'''This module Retrieves the list of all place objects,
deletes, updates, creates and gets information of a place '''
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_all_place(city_id):
    ''' retreive all place associated with the city id '''
    city_objs = storage.all('City')
    key = 'City.{}'.format(city_id)

    if key in city_objs:
        city = city_objs.get(key)
        return jsonify([obj.to_dict() for obj in city.places])

    abort(404)


@app_views.route('/places/<place_id>/', strict_slashes=False)
def get_a_place(place_id):
    '''return the place with matching id'''
    place_objs = storage.all('Place')
    key = 'Place.{}'.format(place_id)

    if key in place_objs:
        place = place_objs.get(key)
        return jsonify(place.to_dict())

    abort(404)


@app_views.route('/places/<place_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' delete place matching the id'''
    place_objs = storage.all('Place')
    key = 'Place.{}'.format(place_id)

    if key in place_objs:
        obj = place_objs.get(key)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    ''' create a place '''

    data = request.get_json()
    city_objs = storage.all('City')
    key = 'City.{}'.format(city_id)

    if key not in city_objs:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    if data.get('user_id') is None:
        abort(400, "Missing user_id")

    user_objs = storage.all('User')
    user_id = data.get('user_id')
    if 'User.{}'.format(user_id) not in user_objs:
        abort(404)
    if data.get('name') is None:
        abort(400, "Missing name")

    data["city_id"] = city_id
    place_obj = Place(**data)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    ''' update place  whose id is passed'''

    data = request.get_json()
    place_objs = storage.all('Place')
    key = 'Place.{}'.format(place_id)

    if key not in place_objs:
        abort(404)

    if data is None:
        abort(400, "Not a JSON")

    place = place_objs.get(key)
    for k, v in data.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_place():
    ''' serach for place object depending on the pararameters passed'''
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if not data or (not data.get("states") and not data.get("cities")
                    and not data.get("amenities")):
        place_objs = storage.all('Place')
        return jsonify([obj.to_dict() for obj in place_objs.values()])

    place_inState = []
    if data.get("states"):
        for state_id in data.get("states"):
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places = city.places
                    place_inState.extend(places)

    if data.get("cities"):
        for city_id in data.get("cities"):
            city = storage.get(City, city_id)
            if city:
                places = city.places
                place_inState.extend(places)

    place_inState = list(set(place_inState))  # remove dups

    if data.get("amenities"):
        place_with_amenity = []
        if data.get("states") or data.get("cities"):
            place_objs = place_inState
        else:
            place_objs = storage.all('Place').values()
        for place in place_objs:
            if place.amenities == data.get("amenities"):
                place_with_amenity.append(place)
        return jsonify([obj.to_dict() for obj in place_with_amenity])

    return jsonify([obj.to_dict() for obj in place_inState])

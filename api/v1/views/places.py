#!/usr/bin/python3
"""view for places objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, storage_t
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from tkinter import N


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all places given an City"""
    places_list = []
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for place in city.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id):
    """Retrieves a place by a given ID"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_place(place_id):
    """Deletes a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
    )
def create_place(city_id):
    """Creates a place object"""
    request_data = request.get_json()
    state = storage.get("City", city_id)
    if state is None:
        abort(404)
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', request_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    name = request.get_json().get('name')
    user_id = request.get_json().get('user_id')
    obj = Place(name=name, user_id=user_id, city_id=city_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Update api/v1/views/places.py to add a new endpoint:
    POST /api/v1/places_search that retrieves all Place
    objects depending of the JSON in the body of the request.
    """

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    keys = body.keys()
    if len(body) <= 0\
       or (('states' not in keys or len(body['states']) <= 0) and
       ('cities' not in keys or len(body['cities']) <= 0)):
        if 'amenities' not in keys:
            places = storage.all(Place).values()
            dcts = [pl.to_dict() for pl in places]
            if storage_t == 'db':
                for idx in range(len(dcts)):
                    if 'amenities' in dcts[idx].keys():
                        del dcts[idx]['amenities']
            return jsonify(dcts)
        else:
            places = storage.all(Place).values()
            unwanted = []
            for idx, place in enumerate(places):
                if storage_t == 'db':
                    amens_ids = [m.id for m in place.amenities]
                else:
                    amens_ids = place.amenity_ids
                for amenity_id in body['amenities']:
                    if amenity_id not in amens_ids:
                        unwanted.append(idx)
                        break
            for i in unwanted:
                del places[i]
            dcts = [pl.to_dict() for pl in places]
            if storage_t == 'db':
                for idx in range(len(dcts)):
                    if 'amenities' in dcts[idx].keys():
                        del dcts[idx]['amenities']
            return jsonify(dcts)

    places = storage.all(Place).values()
    wanted_places = []
    cities = {}

    if 'cities' in keys:
        for cityId in body['cities']:
            cities[cityId] = cityId

    if 'states' in keys:
        for state in storage.all(State).values():
            if state.id in body['states']:
                for city in state.cities:
                    cities[city.id] = city.id

    for place in places:
        if len(cities) > 0:
            if place.city_id in cities:
                wanted_places.append(place)
    unwanted = []
    if 'amenities' in keys:
        for idx, place in enumerate(wanted_places):
            if storage_t == 'db':
                amens_ids = [m.id for m in place.amenities]
            else:
                amens_ids = place.amenity_ids
            for amenity_id in body['amenities']:
                if amenity_id not in amens_ids:
                    unwanted.append(idx)
                    break

    for i in unwanted:
        del wanted_places[i]
    dcts = [pl.to_dict() for pl in wanted_places]
    if storage_t == 'db':
        for idx in range(len(dcts)):
            if 'amenities' in dcts[idx].keys():
                del dcts[idx]['amenities']
    return jsonify(dcts)

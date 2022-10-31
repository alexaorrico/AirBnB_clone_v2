#!/usr/bin/python3
"""
a new view for Place objects that handles
all default RESTFul API actions:
"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False
)
def all_places(city_id):
    city = storage.all(City, city_id)
    place_list = []

    if city is None:
        raise NotFound

    places = city.places

    for place in places.items():
        place_list.append(place.to__dict())
    return make_response(jsonify(place_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    return make_response(jsonify(place.to__dict()), 200)


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_place(place_id):
    

    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
)
def add_place(city_id):
   
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    if 'user_id' not in request.get_json().keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User, request.get_json()['user_id'])

    if user is None:
        raise NotFound

    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)

    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    
    place = storage.get(Place, place_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if place is None:
        raise NotFound

    for key, plac in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            place.__setattr__(key, plac)

    place.save()

    return make_response(jsonify(place.to__dict()), 200)

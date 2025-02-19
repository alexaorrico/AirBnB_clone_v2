#!/usr/bin/python3
'''places file'''
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_city(city_id):
    '''return places of a city'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    places_city = []
    for place in places.values():
        if place.city_id == city.id:
            places_city.append(place.to_dict())
    return jsonify(places_city)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def req_place(place_id):
    '''gets a specific place'''
    try:
        place = storage.get(Place, place_id)
    except KeyError:
        abort(404)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    '''deletes a specific place'''
    try:
        place = storage.get(Place, place_id)
    except KeyError:
        abort(404)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    '''post a place'''
    if request.content_type != "application/json":
        abort(400, 'Not a JSON')
    try:
        city = storage.get(City, city_id)
    except KeyError:
        abort(404)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    try:
        user = storage.get(User, user_id)
    except KeyError:
        abort(404)
    if user is None:
        abort(404)
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''update a specific place'''
    try:
        place = storage.get(Place, place_id)
    except KeyError:
        abort(404)
    if place is None:
        abort(404)
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())

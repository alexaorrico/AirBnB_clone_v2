#!/usr/bin/python3
'''
Import Blueprint to create routes for Amenity
'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    '''Get all Places from a city'''
    city = storage.get(City, city_id)
    places = []

    if city is None:
        abort(404)
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    '''Show a place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete a place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Create a place'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, {'Not a JSON'})
    if 'user_id' not in req:
        abort(400, {'Missing user_id'})
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if 'name' not in req:
        abort(400, {'Missing name'})
    req['city_id'] = city_id
    new_place = Place(**req)
    storage.new(new_place)
    storage.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a place'''
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, {'Not a JSON'})
    for k, v in req.items():
        if k not in ignore:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)

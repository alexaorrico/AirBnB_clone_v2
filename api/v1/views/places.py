#!/usr/bin/python3
"""View for State objects that handles all default RestFul API"""
from api.v1.views import app_views
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET\
    '], strict_slashes=False)
def get_places(city_id):
    """Returns a json object with all the city"""
    list_dict = []
    for obj in storage.all(State).values():
        list_dict.append(obj.to_dict())
    return jsonify(list_dict), 200


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(state_id):
    """Returns a json object with the place with given id"""
    obj = storage.get(Place, place_id)
    if (obj):
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(state_id):
    """Delete a place"""
    obj = storage.get(Place, place_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST\
    '], strict_slashes=False)
def createPlace(city_id):
    """Create a place for a city if not error 404
    """
    cities = storage.get('City', city_id)
    if not cities:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place.keys():
        abort(400, {'Missing user_id'})
    userid = storage.get('User', place['user_id'])
    if not userid:
        abort(404)
    if 'name' not in place:
        abort(400, {'Missing name'})
    new_place = Place(**place)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    places = storage.get('Place', place_id)
    if not places:
        abort(404)

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place.items():
        if key not in ignore:
            setattr(places, key, value)
    storage.save()
    return jsonify(places.to_dict()), 200

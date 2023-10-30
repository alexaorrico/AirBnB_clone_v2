#!/usr/bin/python3
"""
view for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False)
def get_place_city(city_id):
    """
    Retrieves the list of all City objects of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = city.places
    places_serializable = []
    for city in all_places:
        places_serializable.append(city.to_dict())
    return jsonify(places_serializable)


@app_views.route('/places/<place_id>',
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a City object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in content:
        abort(400, 'Missing user_id')
    user = storage.get(User, content['user_id'])
    if user is None:
        abort(404)
    if 'name' not in content:
        abort(400, 'Missing name')
    place = Place(**content)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Updates a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    skip = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in skip:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

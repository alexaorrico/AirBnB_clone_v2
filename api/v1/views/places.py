#!/usr/bin/python3
""" This module handles all default RESTFUL api actions for Place objects"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_place(city_id):
    """ Retrieves list of all place objects of a city """
    place_lists = []
    """for objects in storage.all(Amenity).values():
        amenity_objects = objects.to_dict()
        amenity_lists.append(amenity_objects)
    return jsonify(amenity_lists)"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        place_lists.append(place.to_dict())
    return place_lists


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_single_place(place_id):
    """ Retrieves a single Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_object(place_id):
    """ Deletes a place object """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place_object(city_id):
    """ Creates a Place """
    data = request.get_json()
    cityId = storage.get(City, city_id)
    if not cityId:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data['city_id'] = city_id
    data['user_id'] = user_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place_object(place_id):
    """ Updates a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    data.pop('id', None)
    data.pop('user_id', None)
    data.pop('city_id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

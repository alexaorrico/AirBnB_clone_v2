#!/usr/bin/python3
"""
Places
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """
    Retrieves the list of all Places objects of the City
    """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    places_list = []
    for place in cities.places:
        places_list.append(place.to_dict())
    return(jsonify(places_list))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "user_id" not in request.get_json():
        no_user_id = {"error": "Missing user_id"}
        return (jsonify(no_user_id), 400)
    user = storage.get(User, city.user_id)
    if user is None:
        abort(404)
    if "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    obj_dict = request.get_json()
    obj_dict['city_id'] = city.id
    obj_dict['user_id'] = user.id
    place = Place(**obj_dict)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at',
                   'updated_at']
    for key in obj_dict.keys():
        if key not in ignore_keys:
            setattr(place, key, obj_dict[key])
    place.save()
    return (jsonify(place.to_dict()), 200)

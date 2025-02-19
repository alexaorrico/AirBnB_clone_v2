#!/usr/bin/python3
""" script for views """

from models import storage
from models.place import Place
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort
from flask import request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_place(city_id):
    """Route that returns all place"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    all_list = []
    for place in city_obj.places:
        all_list.append(place.to_dict())

    return make_response(jsonify(all_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Route that returns a place by its ID"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    return make_response(jsonify(place_obj.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ delete http request"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """post http request """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    request_dict = request.get_json()
    request_dict['city_id'] = city_id
    obj = Place()

    for k, v in request_dict.items():
        setattr(obj, k, v)

    # add obj to current DB session and save it.
    storage.new(obj)
    storage.save()
    new_state = obj.to_dict()
    return make_response(jsonify(new_state), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_update(place_id):
    """put http request"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    new_dict = request.get_json()
    ignore_keys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for k, v in new_dict.items():
        if k not in ignore_keys:
            setattr(place_obj, k, v)

    storage.save()
    return make_response(jsonify(place_obj.to_dict()), 200)

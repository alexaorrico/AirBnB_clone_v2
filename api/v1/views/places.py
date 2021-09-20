#!/usr/bin/python3
"""creates a new view for State Objects"""
from models.place import Place
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
import json


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """gets all state objects"""
    city = storage.get(City, city_id)
    if city:
        single_objs = []
        for place in city.places:
            single_objs.append(place.to_dict())
        return jsonify(single_objs)
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a new place"""
    if request.json:
        new_dict = request.get_json()
        city = storage.get(City, city_id)
        if city:
            if "user_id" in new_dict.keys():
                user = storage.get(User, new_dict['user_id'])
                if user:
                    if "name" in new_dict.keys():
                        new_dict['city_id'] = city_id
                        new_place = Place(**new_dict)
                        storage.new(new_place)
                        storage.save()
                        return jsonify(new_place.to_dict()), 201
                    else:
                        abort(400, description="Missing name")
                abort(404)
            else:
                abort(400, description="Missing user_id")
        abort(404)
    else:
        abort(400, description="Not a JSON")


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """gets the state object using his id"""
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    else:
         return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Deletes"""
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """PUT"""
    res = request.get_json()
    if not res:
        abort(400, {"Not a JSON"})
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    i_key = ["id", "created_at", "updated_at"]
    for key, value in res.items():
        if key not in i_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

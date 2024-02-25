#!/usr/bin/python3
"""
cities.py
"""
from . import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from flask import abort, request, Response, make_response
import json


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_per_id(state_id):
    """
    Retrieves the list of all City
    objects of a State
    """
    desired_cities = []
    for key, value in storage.all(City).items():
        if value.state_id == state_id:
            desired_cities.append({key: value})
    if desired_cities != []:
        return jsonify(desired_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """
    retrieves one city per id
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    deletes city
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def POST_city(state_id):
    """
    add city
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    obj = City()
    try:
        new_city = obj()
        setattr(new_city, "state_id", state_id)
        setattr(new_city, "name", request.json["name"])
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    except BaseException:
        abort(404)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    updates city
    """
    object_ = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at", "state_id"]
    for obj in storage.all("City").values():
        if obj.id == city_id:
            object_ = obj
            for key, value in request.json.items():
                if key not in check:
                    setattr(obj, key, value)
                    obj.save()
    if not object_:
        abort(404)
    return object_.to_dict(), 200

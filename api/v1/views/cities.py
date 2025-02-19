#!/usr/bin/python3
"""
Module creates an api view for City objects
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_to_city_index(state_id):
    """
    Retrieves all cities under state state_id on
    GET /api/v1/states/<state_id>/cities
    """
    parent_obj = storage.get(State, state_id)
    if parent_obj is None:
        abort(404)
    else:
        all_cities_raw = parent_obj.cities
        all_cities = []
        for city in all_cities_raw:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieves city object by its id on
    GET /api/v1/cities/<city_id>
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    Deletes a city object on
    DELETE /api/v1/cities/<city_id> request
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    Replaces a city object on
    PUT /api/v1/cities/<city_id> request
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
                obj.save()
            return city_by_id(city_id), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Posts a city object and adds it to its parent state
    POST /api/v1/states/<state_id>/cities request
    """
    parent_obj = storage.get(State, state_id)
    if parent_obj is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'name' in json.keys():
            obj = City(**json)
            obj.state_id = state_id
            obj_id = obj.id
            obj.save()
            return city_by_id(obj_id), 201
        else:
            abort(400, description='Missing name')

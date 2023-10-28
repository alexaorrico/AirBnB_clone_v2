#!/usr/bin/python3
"""
City
"""

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<string:id>/cities', methods=["GET"])
def cities_by_state(id):
    """GET cities by state id"""
    state = storage.get(State, id)
    if state is None:
        abort(404)
    if state.cities is None:
        abort(404)
    else:
        cities = state.cities
        cities_list = []
        for city in cities:
            cities_list.append(city.to_dict())
    return (jsonify(cities_list))


@app_views.route('/cities/<string:id>', methods=["GET"])
def city(id):
    """GET City by id"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route('/cities/<string:id>', methods=["DELETE"])
def remove_city(id):
    """REMOVE City by id"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route('/states/<string:id>/cities/', methods=["POST"])
def create_city(id, strict_slashes=False):
    """CREATE City for state by id"""
    if request.is_json:
        json_city = request.get_json()
        if json_city.get("name") is None:
            abort(400, description="Missing name")
        else:
            if storage.get(State, id) is None:
                abort(404)
            json_city["state_id"] = id
            new_city = City(**json_city)
            storage.new(new_city)
            storage.save()
            return new_city.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/cities/<string:id>', methods=["PUT"])
def update_city(id):
    """UPDATE City by id"""
    city = storage.get(City, id)
    if city is None:
        abort(404)
    if request.is_json:
        forbidden = ["id", "created_at", "updated_at"]
        city_json = request.get_json()
        storage.delete(city)
        for k, v in city_json.items():
            if city_json[k] not in forbidden:
                setattr(city, k, v)
        storage.new(city)
        storage.save()
        return city.to_dict(), 200
    else:
        abort(400, description="Not a JSON")

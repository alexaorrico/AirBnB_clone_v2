#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_citystate(state_id=None):
    """take cities from each state"""
    if storage.get(State, state_id) is None:
        abort(404)
    citystate = []
    for c in storage.get(State, state_id).cities:
        citystate.append(c.to_dict())
    return jsonify(citystate)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """get city object"""
    if storage.get(City, city_id) is None:
        abort(404)
    else:
        return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id=None):
    """delete city object"""
    if storage.get(City, city_id):
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """add city object"""
    if storage.get(State, state_id) is None:
        abort(404)
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        new_city = City(**request.get_json())
        storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """change city object"""
    if storage.get("City", city_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "state_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("City", city_id), key, value)
    storage.save()
    return jsonify(storage.get("City", city_id).to_dict()), 200

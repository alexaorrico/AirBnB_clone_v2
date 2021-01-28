#!/usr/bin/python3
""" Module cities """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_getstate(state_id=None):
    """Retrieve list city objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = []
    for i in state.cities:
        list_cities.append(i.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """get city objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Delete City"""
    if storage.get(City, city_id):
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ post method """
    if storage.get(State, state_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif "name" not in data.keys():
        abort(400, "Missing name")
    else:
        new_cit = City(**data)
        storage.save()
    return jsonify(new_cit.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """Put method"""
    data = request.get_json()
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if data is None:
        return "Not a JSON", 400
    for k, v in data.items():
        if k in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200

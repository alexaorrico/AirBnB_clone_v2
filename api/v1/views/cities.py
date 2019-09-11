#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities')
def cities(state_id):
    """get state with his id"""
    for val in storage.all("State").values():
        if val.id == state_id:
            return jsonify(list(map(lambda v: v.to_dict(), val.cities)))
    abort(404)


@app_views.route('/cities/<city_id>')
def city_id(city_id):
    """get state with his id"""
    for val in storage.all("City").values():
        if val.id == city_id:
            return jsonify(val.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def cities_delete(city_id):
    """delete a obj with his id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_create(state_id):
    """create city object"""
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    if "name" not in data:
        msg = "Missing name"
        return jsonify({"error": msg}), 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data.update({'state_id': state_id})
    city = City(**data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_update(city_id):
    """update state"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
    else:
        msg = "Not a JSON"
        return jsonify({"error": msg}), 400

    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, k, v)

    storage.save()
    return jsonify(city.to_dict()), 200

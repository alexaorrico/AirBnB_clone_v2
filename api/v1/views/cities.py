#!/usr/bin/python3
"""Script that handls City objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """retrieves all City objects from a specific state
    Args:
        state_id: state id"""
    list_of_cities = []
    objs = storage.get("State", str(state_id))
    if objs is None:
        abort(404)
    for obj in objs.cities:
        list_of_cities.append(obj.to_dict())
    return jsonify(list_of_cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """create city route
    Args:
        state_id: state id"""
    json_cts = request.get_json(silent=True)
    if json_cts is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in json_cts:
        abort(400, 'Missing name')
    json_cts["state_id"] = state_id
    new_city = City(**json_cts)
    new_city.save()
    response = jsonify(new_city.to_dict())
    response.status_code = 201
    return response


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """gets a specific City object by ID
    Args:
        city_id: city object id"""
    objs = storage.get("City", str(city_id))
    if objs is None:
        abort(404)
    return jsonify(objs.to_dict())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """updates specific City object by ID
    Args:
        city_id: city object ID"""
    json_cts = request.get_json(silent=True)
    if json_cts is None:
        abort(400, 'Not a JSON')
    objs = storage.get("City", str(city_id))
    if objs is None:
        abort(404)
    for key, val in json_cts.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(objs, key, val)
    objs.save()
    return jsonify(objs.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """deletes City by id
    Args:
        city_id: city object id"""
    objs = storage.get("City", str(city_id))
    if objs is None:
        abort(404)
    storage.delete(objs)
    storage.save()
    return jsonify({})

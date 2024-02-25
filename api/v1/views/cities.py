#!/usr/bin/python3
"""
Cities view
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, abort, request


@app_views('/states/<state_id>/cities', methods=["GET"])
def get_city_via_state(state_id):
    """Gets City via the state"""
    city_obj_list = []
    found_state = storage.get('State', str(state_id))

    if found_state is None:
        abort(404)

    for obj in found_state.cities:
        city_obj_list.append(obj.to_dict())

    return jsonify(city_obj_list)


@app_views('/cities/<city_id>', methods=["GET"])
def get_city(city_id):
    """Gets City based on the city ID"""
    found_city = storage.get("City", str(city_id))
    if found_city is None:
        abort(404)
    resp = jsonify(found_city.to_dict())
    resp.status_code = 200
    return resp


@app_views('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """Deletes the given city using the id"""
    found_city = storage.get("City", str(city_id))
    if found_city is None:
        abort(404)

    storage.delete(found_city)
    storage.save()
    return ({})


@app_views('/states/<state_id>/cities', methods=["POST"])
def create_city(state_id):
    """Creates city for a given state"""
    new_city = request.get_json()
    if new_city is None:
        abort(400, "Not a JSON")

    found_state = storage.get("State", str(state_id))
    if found_state is None:
        abort(404)

    if "name" not in new_city:
        abort(400, "Missing name")

    new_city["state_id"] = state_id

    instance_city = City(**new_city)
    instance_city.save()
    resp = jsonify(instance_city.to_json())
    resp.status_code = 201
    return resp


@app_views('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """Updates a given city"""
    fetched_city = storage.get("City", str(city_id))
    if fetched_city is None:
        abort(404)
    updates_city = request.get_json()
    if updates_city is None:
        abort(400, "Not a JSON")

    for key, value in updates_city.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_city, key, value)
    fetched_city.save()
    resp = jsonify(fetched_city.to_dict())
    resp.status_code = 200
    return resp

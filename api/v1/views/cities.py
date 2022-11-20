#!/usr/bin/python3
"""Contains functions that Handle all requests to the city endpoint."""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import city, state, storage


@app_views.route("/cities", strict_slashes=False,
                 defaults={'city_id': None},
                 methods=['GET'])
@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id):
    """Handles get, put and delete requests to the cities endpoint"""
    if request.method == "GET":
        if city_id is None:
            return [obj.to_dict() for obj in storage.all(city.City).values()]
        elif city_id is not None:
            ci_obj = storage.get("City", city_id)
            if not ci_obj:
                abort(404)
            return jsonify(obj.to_dict())
    elif request.method == "PUT":
        try:
            put_data = request.get_json()
        except Exception:
            return make_response("Not a JSON", 400)
        ci_obj = storage.get("City", city_id)
        if not ci_obj:
            abort(404)
        for key, value in put_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(ci_obj, key, value)
        ci_obj.save()
        return make_response(jsonify(ci_obj.to_dict()), 200)
    elif request.method == "DELETE":
        ci_obj = storage.get("City", city_id)
        if ci_obj is None:
            abort(404)
        ci_obj.delete()
        storage.save()
        return (jsonify({}))


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
def get_state_cities(state_id):
    """Handles get requests to states cities."""
    st_obj = storage.get("State", state_id)
    if not st_obj:
        abort(404)
    return [ci_obj.to_dict() for ci_obj in storage.all(city.City).values()\
            if ci_obj.state_id == state_id]


@app_views.route("/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def post_state_cities(state_id):
    """Handles post requests to states cities."""
    st_obj = storage.get("State", state_id)
    if not st_obj:
        abort(404)
    try:
        post_data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)
    if 'name' not in post_data:
        return make_response("Missing name", 400)
    new_city = city.City()
    new_city.state_id = state_id
    new_city.name = post_data['name']
    new_city.save()
    return make_response(new_city.to_dict(), 201)

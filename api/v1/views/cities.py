#!/usr/bin/python3
"""Module for City related endpoints"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """GET /state api route"""
    state = storage.get("State", state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify([c.to_dict() for c in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """GET /city api route"""
    city = storage.get("City", city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """DELETE /city api route"""
    city = storage.get("City", city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """POST /cities api route"""
    state = storage.get("State", state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data['state_id'] = state_id
    c = City(**data)
    c.save()
    return make_response(jsonify(c.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """PUT /cities api route"""
    city = storage.get("City", city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

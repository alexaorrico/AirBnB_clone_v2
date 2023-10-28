#!/usr/bin/python3
"""this view hundles states endpoints"""
from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from flask import make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def all_cities_for_state(state_id):
    """gets all cities instances"""
    d_state = storage.get(State, state_id)

    if d_state:
        cities = storage.all(City).values()
        cities_l = []
        for city in cities:
            if city.state_id == state_id:
                cities_l.append(city.to_dict())
        return jsonify(cities_l)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_c(city_id):
    """ gets state with the given id"""
    d_city = storage.get(City, city_id)
    if d_city:
        return jsonify(d_city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes city with the given id"""
    d_city = storage.get(City, city_id)
    if d_city:
        storage.delete(d_city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """create new city with the supplied data"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data["state_id"] = state_id
    new = City(**data)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """updates city with supplied id"""
    d_city = storage.get(City, city_id)

    if not d_city:
        abort(404)

    if request.get_json():
        data = request.get_json()
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(d_city, k, v)
        d_city.save()
        return make_response(jsonify(d_city.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)

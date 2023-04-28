#!/usr/bin/python3

"""handles all default RESTFul API actions on cities"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<string:state_id>/cities", methods=["GET", "POST"])
def state_cities(state_id):
    """handles all default RESTFul API actions on cities"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
        return

    if request.method == "GET":
        all_cities = []
        for city in state.cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)

    elif request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        elif "name" not in request.get_json():
            return make_response(jsonify({"name": "Missing name"}), 400)
        new_dict = request.get_json()
        new_dict["state_id"] = state_id
        new_city = City(**new_dict)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["GET", "PUT", "DELETE"])
def cities(city_id):
    """ handles all default RESTFul API actions on cities"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
        return

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})

    elif request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        new_dict = request.get_json()
        for key, value in new_dict.items():
            if key not in ["id", "state_id", "created_at", "update_at"]:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)

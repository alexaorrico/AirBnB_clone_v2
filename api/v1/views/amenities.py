#!/usr/bin/python3
"""restful API functions for State"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import request, jsonify, abort


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=["GET", "POST"]
                 )
def states_end_points(state_id):
    """state objects that handles all default RESTFul API actions"""
    obj_states = storage.all(State)
    states_dict = [obj.to_dict() for obj in obj_states.values()]
    if request.method == "GET":
        for obj in states_dict:
            if obj.get('id') == state_id:
                obj_cities = storage.all(City)
                cities_dict = [obj.to_dict() for obj in
                               obj_cities.values() if
                               obj.state_id == state_id]
                return jsonify(cities_dict)
        abort(404)

    elif request.method == "POST":
        for obj in states_dict:
            if obj.get('id') == state_id:
                my_dict = request.get_json()
                if not my_dict or type(my_dict) is not dict:
                    abort(400, "Not a JSON")
                elif not my_dict["name"]:
                    abort(400, "Missing name")
                else:
                    my_dict["state_id"] = state_id
                    new_city = City(**my_dict)
                    new_city.save()
                    return jsonify(new_city.to_dict()), 201
        abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=["DELETE", "PUT", "GET"])
def city_end_points(city_id):
    """state objects that handles all default RESTFul API actions"""
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_city.to_dict())
    elif request.method == "DELETE":
        storage.delete(obj_city)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        get_new_name = request.get_json()
        if not get_new_name or type(get_new_name) is not dict:
            abort(400, "Not a JSON")
        obj_cityname = get_new_name.get("name")
        obj_city.save()
        return jsonify(obj_city.to_dict()), 200

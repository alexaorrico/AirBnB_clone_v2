#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id=None):
    """ list all state"""
    get_states = storage.get(State, state_id)
    list_cities = []
    if get_states:
        for city in get_states.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route("/cities/<city_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_id_city(city_id=None):
    """ Return a city object """
    city_ob = storage.get(City, city_id)
    if city_ob:
        return jsonify(city_ob.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ Delete A city """
    city_ob = storage.get(City, city_id)
    if city_ob:
        storage.delete(city_ob)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """ Create a City object """
    state_ob = storage.get(State, state_id)
    data = request.get_json()
    if state_ob:
        if data:
            if "name" in data:
                new_city = City(**data)
                setattr(new_city, "state_id", state_id)
                new_city.save()
                return (jsonify(new_city.to_dict()), 201)
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route("/cities/<city_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """ Update a City object """
    up_date = storage.get(City, city_id)
    data = request.get_json()
    if up_date:
        if data:
            if "name" in data:
                for k, v in data.items():
                    ignore = ["id", "created_at", "updated_at"]
                    if k != ignore:
                        setattr(up_date, k, v)
                up_date.save()
                return jsonify(up_date.to_dict())
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)

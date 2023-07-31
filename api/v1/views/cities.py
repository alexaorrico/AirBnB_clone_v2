#!/usr/bin/python3
"""
A new view for City objects that handles all default RESTFul API actions
"""
from flask import abort
from flask import jsonify
from flask import request

from . import City
from . import State
from . import storage
from . import app_views

# f are class properties to validate the request payload
f = ("name",)


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def cities_by_state(state_id):
    """
    Creates a new City obj
    Retrieves the list of all City objects of a State
    Args:
        state_id: primary key of an existing state object
    """
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([c.to_dict() for c in state.cities])
    else:
        body = request.get_json(silent=True)
        if request.is_json and body is not None:
            pay = {k: str(v) for k, v in body.items() if k in f}
            if not pay.get("name", None):
                abort(400, description="Missing name")
            pay.update({"state_id": str(state_id)})
            new_city = City(**pay)
            storage.new(new_city), storage.save()
            return jsonify(new_city.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def one_city(city_id):
    """
    Deletes an existing City object
    Retrieves an existing City object
    Updates an existing City object
    Args:
        city_id: primary key of an existing city object
    """
    city = storage.get(City, str(city_id))
    if not city:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city), storage.save()
        return jsonify({})
    else:
        body = request.get_json(silent=True)
        if request.is_json and body:
            [setattr(city, k, str(v)) for k, v in body.items() if k in f]
            city.save()
            return jsonify(city.to_dict()), 200
        abort(400, description="Not a JSON")

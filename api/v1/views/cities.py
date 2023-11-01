#!/usr/bin/python3
"""cities added to the database or deleted from the database"""

from flask import jsonify, request, abort
from . import app_views, City, State, storage

pl = ("name",)


@app_views.route("/states/<state_id>/cities",
                 methods=["GET", "POST"], strict_slashes=False)
def post_state(state_id):
    """ Adds a new state to the list of states available"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify([list.to_dict() for list in state.cities])
    else:
        data = request.get_json(silent=True)
        if request.is_json and data is not None:
            load = {key: str(value) for key, value in data.items()
                    if key in pl}
            if not load.get("name", None):
                abort(400, description="Missing name")
            load.update({"state_id": str(state_id)})
            cty = City(**load)
            storage.new(cty), storage.save()
            return jsonify(cty.to_dict()), 201
        abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Removes a city from the database and returns it."""
    deleted_city = storage.get(City, str(city_id))
    if not deleted_city:
        abort(404, description="Not found")
    if request.method == "GET":
        return jsonify(deleted_city.to_dict())
    elif request.method == "DELETE":
        storage.delete(deleted_city), storage.save()
        return jsonify({})
    else:
        data = request.get_json(silent=True)
        if request.is_json and data:
            [setattr(deleted_city, key, str(value))
             for key, value in data.items() if key in pl]
            deleted_city.save()
            return jsonify(deleted_city.to_dict()), 200
        abort(400, description="Not a JSON")

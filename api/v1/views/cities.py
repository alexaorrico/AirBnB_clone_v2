#!/usr/bin/python3
"""modify state objects via APIs"""
from models.state import State
from models.city import City
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["GET"])
def get_state_cities(state_id=None):
    """etrieves the list of all City objects of a State:
       GET /api/v1/states/<state_id>/cities
    """
    state = abortNotExists(State, state_id)
    cities_dicts_list = []
    for city in state.cities:
        cities_dicts_list.append(city.to_dict())
    return jsonify(cities_dicts_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id=None):
    """retrieve a city object"""
    # if not city_id:
    #     objs_dict = storage.all(City)
    #     obj_list = []
    #     for obj in objs_dict.values():
    #         obj_list.append(obj.to_dict())
    #     return make_response(jsonify(obj_list))

    # else:
    obj = abortNotExists(City, city_id)
    return make_response(jsonify(obj.to_dict()))


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def post_city(state_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""
    abortNotExists(State, state_id)
    try:
        data = request.get_json()
        data["state_id"] = state_id
    except Exception:
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")

    new_obj = City(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object:: DELETE /api/v1/cities/<city_id>"""
    obj = abortNotExists(City, city_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id):
    """Updates a City object: PUT /api/v1/cities/<city_id>"""
    obj = abortNotExists(City, city_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)

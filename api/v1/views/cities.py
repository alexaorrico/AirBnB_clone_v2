#!/usr/bin/python3
""" City api views
"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


# read
@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ gets all cities in a state

    Args:
        state_id (str): state id
    """

    # get state by id
    city_list = []
    state = storage.get("State", str(state_id))
    if not state:
        abort(404)

    # get all cities related to the state_id
    for city in state.cities:
        city_list.append(city.to_dict())

    return jsonify(city_list), 200

# read


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_cities_id(city_id):
    """ Gets city by id

    Args:
        city_id (str): city id
    """
    city = storage.get("City", str(city_id))

    if not city:
        abort(404)

    return jsonify(city.to_dict()), 200


# delete
@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city

    Args:
        city_id (str): City id
    """
    # get the city
    city = storage.get("City", str(city_id))

    if not city:
        abort(404)

    # delete and save
    storage.delete(city)
    storage.save()

    # return an empty json dict
    return jsonify({}), 200


# Create
@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ adds new city instance entry

    Args:
        state_id (str): state id
    """
    # get key value parameters from post
    params_json = request.get_json(silent=True)

    if not params_json:
        abort(400, "Not a JSON")

    # get state
    state = storage.get("State", str(state_id))

    if not state:
        abort(404)

    # if missing required data name
    if "name" not in params_json:
        abort(400, "Missing name")

    params_json["state_id"] = state_id

    new_city = City(**params_json)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


# Update
@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Update a city

    Args:
        city_id (str): City id
    """
    # get params
    params_json = request.get_json(silent=True)
    # if none or not a json
    if not params_json:
        abort(400, "Not a JSON")

    # check if the city exist
    city = storage.get("City", str(city_id))
    if not city:
        abort(404)

    for k, v in params_json.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, k, v)

    city.save()
    return jsonify(city.to_dict()), 200

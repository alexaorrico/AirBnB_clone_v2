#!/usr/bin/python3
"""RESTful API view to handle actions for 'City' objects"""

from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def state_cities_routes(state_id):
    """
    GET: Retrieves the list of all City objects in the state where
         id == state_id
    POST: Creates a City in the state where id == state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "GET":        
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == "POST":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        name = in_data.get("name")
        if name is None:
            return "Missing name\n", 400

        in_data["state_id"] = state_id
        city = City(**in_data)
        city.save()
        return city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def city_id_routes(city_id):
    """
    GET: Retrieves the City where id == city_id
    PUT: Updates the City that has id == city_id
    PUT: Deletes the City that has id == city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())

    elif request.method == "PUT":
        in_data = request.get_json(silent=True)
        if in_data is None or not isinstance(in_data, dict):
            return 'Not a JSON\n', 400

        for key, val in in_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, val)
        city.save()
        return city.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

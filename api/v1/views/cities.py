#!/usr/bin/python3
"""HolbertonBnB City view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
@swag_from("../apidocs/cities/get_cities.yml", methods=["GET"])
@swag_from("../apidocs/cities/post.yml", methods=["POST"])
def cities_by_state(state_id):
    """Defines GET and POST methods for cities on the states route.

    GET - Retrieve a list of City objects related to a given State.
    POST - Creates a City.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])

    # POST method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if data.get("name") is None:
        return "Missing name", 400
    data["state_id"] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
@swag_from("../apidocs/cities/get_city_id.yml", methods=["GET"])
@swag_from("../apidocs/cities/delete.yml", methods=["DELETE"])
@swag_from("../apidocs/cities/put.yml", methods=["PUT"])
def city_id(city_id):
    """Defines GET, DELETE and PUT methods for a specific ID on cities.

    GET - Retrieves a City object with the given id.
    DELETE - Deletes the City object with the given id.
    PUT - Updates the City object with a given JSON object of key/value pairs.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    # GET method
    if request.method == "GET":
        return jsonify(city.to_dict())

    # DELETE method
    elif request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})

    # PUT method
    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "state_id", "created_at", "updated_at"}
    [setattr(city, k, v) for k, v in data.items() if k not in avoid]
    city.save()
    return jsonify(city.to_dict())

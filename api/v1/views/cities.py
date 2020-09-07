#!/usr/bin/python3
"""
Define city routes.
"""


from flask import request, abort, jsonify
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities(state_id):
    """Define /cities route with GET and POST methods

    POST - Create a new city
    GET - Get a list of all cities
    """
    state = storage.get('State', state_id)
    if state is None:
        return abort(404)

    # GET
    if request.method == "GET":
        return jsonify([city.to_dict() for city in state.cities])

    # POST
    doc = request.get_json(silent=True)
    if doc is None:
        return "Not a JSON", 400
    if doc.get("name") is None:
        return "Missing name", 400
    doc['state_id'] = state_id
    city = City(**doc)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city(city_id):
    """Define /cities/<city_id> with GET, PUT and DELETE  methodes

    GET - get a city with the given id
    PUT - Update the city with the given id
    DELETE - Deletes the cityy with the givem id
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    # GET
    if request.method == "GET":
        return jsonify(city.to_dict())

    # PUT
    elif request.method == "PUT":
        doc = request.get_json(silent=True)
        if doc is None:
            return "Not a JSON", 400

        for k, v in doc.items():
            if k not in ("id", "created_at", "updated_at"):
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())

    # DELETE
    city.delete()
    city.save()
    return jsonify({})

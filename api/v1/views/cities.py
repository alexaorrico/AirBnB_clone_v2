#!/usr/bin/python3
"""Renders json view for City object(s)
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['GET'])
def cities_of_state(state_id):
    """Returns list of json representation of all cities linked to the given state
    Raises 404 if no state found based on state_id
    """
    state = storage.get("State", state_id)
    if state:
        return jsonify([c.to_dict() for c in state.cities])
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """create a city linked to state specified by state_id
    """
    from models.city import City
    state = storage.get("State", state_id)
    if state:
        body = request.get_json()
        if not body:
            return make_response('Not a JSON', 400)
        if not body.get('name'):
            return make_response('Missing name', 400)
        city = City(name=body.get('name'), state_id=state_id)
        storage.new(city)
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)
    abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Returns json representation of a city
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete a city object from storage
    """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=['PUT'])
def modify_city(city_id):
    """modify a city object
    """
    ignore = ["id", "state_id", "created_at", "updated_at"]
    city = storage.get("City", city_id)
    if city:
        body = request.get_json()
        if not body:
            return make_response('Not a JSON', 400)
        for k, v in body.items():
            if k not in ignore:
                setattr(city, k, v)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    abort(404)

#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State
from flasgger.utils import swag_from


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def cities_by_state(state_id):
    """View function that return city objects by state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def show_city(city_id):
    """Endpoint that return a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """Endpoint that delete a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def insert_city(state_id):
    """Endpoint that insert a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    props = request.get_json()
    if type(props) != dict:
        abort(400, description="Not a JSON")
    if not props.get("name"):
        abort(400, description="Missing name")
    new_city = City(**props)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def update_city(city_id):
    """Endpoint that update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    props = request.get_json()
    if type(props) != dict:
        abort(400, description="Not a JSON")
    for key, value in props.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

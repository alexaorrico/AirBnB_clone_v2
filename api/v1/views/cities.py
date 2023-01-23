#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities',
                 methods=["GET", "POST"], strict_slashes=False)
def get_cities(state_id):
    """get all instances of cities in a state"""
    response = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        for city in state.cities:
            response.append(city.to_dict())
        return (jsonify(response))

    if request.method == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        new_data['state_id'] = state_id
        city = City(**new_data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """get, update and delete city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        response = city.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """delete an instance of city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response

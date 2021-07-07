#!/usr/bin/python3
"""view for City objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects"""
    city = []
    state = storage.get(State, state_id)
    if state:
        for val in state.cities:
            city.append(val.to_dict())
        return jsonify(city)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def obj_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, description='Not a JSON')
    if 'name' not in content:
        abort(400, description='Missing name')
    city = City(name=content['name'], state_id=state_id)
    storage.new(city)
    storage.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        omitir = ['id', 'created_at', 'updated_at']
        for name, value in data.items():
            if name not in omitir:
                setattr(city, name, value)
        storage.save()
        return (jsonify(city.to_dict()), 200)
    else:
        abort(404)

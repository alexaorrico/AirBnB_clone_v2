#!/usr/bin/python3
"""
View for `City` object that handles all default RESTFul API actions
"""
from models import storage
from flask import abort, jsonify, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views, City, State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_city_objects(state_id):
    """returns: a list of all city objects of a state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            city_list = [city.to_dict() for city in state.cities]
            return city_list
    # state_id not linked to any state object
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city_object(city_id):
    """returns: a city object"""
    cities = storage.all(City)
    for city in cities.values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    # obj not found
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city_object(city_id):
    """delete: a city object"""
    cities = storage.all(City)
    for city in cities.values():
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    # object not found
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city_obj(state_id):
    """creates: a city obj:
           returns - the new city created
    """
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            try:
                data = request.get_json()
                # add id to the request data
                data['state_id'] = state_id
            except BadRequest:
                abort(400, "Not a JSON")
            if 'name' not in data:
                abort(400, "Missing name")
            # create object
            new_city = City(**data)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
    # state_id not linked to any state object
    abort(404)


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False)
def update_city_obj(city_id):
    """updates and returns the updated object"""
    objs = storage.all(City)
    for obj in objs.values():
        if obj.id == city_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            for k, v in data.items():
                if k == 'id' or k == 'created_at' or k == 'updated_at':
                    continue
                setattr(obj, k, v)
            storage.save()
            return obj.to_dict(), 200
    # city object not found
    abort(404)

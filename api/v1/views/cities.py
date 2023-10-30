#!/usr/bin/python3
"""Module containing a Flask Blueprint routes that handles
all default RESTFul API actions for City resource"""
from api.v1.views import app_views
from flask import abort, make_response, jsonify, request
from markupsafe import escape
from models import storage
from models.city import City
from models.state import State


def retrive_object(cls, id):
    """Retrives a resource based on given class and id."""
    obj = storage.get(cls, escape(id))
    if obj is None:
        abort(404)
    return (obj)


def validate_request_json(request):
    """Checks validity of request's json content"""
    if not request.is_json:
        abort(make_response(jsonify(error="Not a JSON"), 400))
    req_json = request.get_json()
    if request.method == 'POST' and 'name' not in req_json:
        abort(make_response(jsonify(error="Missing name"), 400))
    return (req_json)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities_get(state_id):
    """Returns a list of cities for a State resource with given id"""
    obj = retrive_object(State, state_id)
    cities = [city.to_dict() for city in obj.cities]
    return (jsonify(cities))


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities_get(city_id):
    """Returns a City resource based on given id"""
    obj = retrive_object(City, city_id)
    return (jsonify(obj.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_delete(city_id):
    """Deletes a City resource based on given id"""
    obj = retrive_object(City, city_id)
    storage.delete(obj)
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def state_cities_post(state_id):
    """Creates a City resource in a State of given id
    if request content is valid."""
    obj = retrive_object(State, state_id)
    req_json = validate_request_json(request)
    req_json['state_id'] = obj.id
    new_city = City(**req_json)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def cities_put(city_id):
    """Updates a City resource of given id if request content is valid."""
    obj = retrive_object(City, city_id)
    req_json = validate_request_json(request)
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()
    return (jsonify(obj.to_dict()))

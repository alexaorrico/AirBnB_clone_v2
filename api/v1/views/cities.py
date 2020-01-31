#!/usr/bin/python3
"""
Handles all default RESTful API actions for City objects
"""

from . import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, make_response, request
from flask.json import jsonify

CITY_IGNORE_KEYS = {'id', 'state_id', 'created_at', 'updated_at'}


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def get_state_cities(state_id):
    """Retrieves the list of all City objects attached to a State"""
    s = storage.get('State', state_id)
    if s is None:
        abort(404)
    return jsonify([c.to_dict() for c in s.cities])


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    """Retrieves a city given its ID"""
    c = storage.get('City', city_id)
    if c is None:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def del_city(city_id):
    """Deletes a city given its ID"""
    c = storage.get('City', city_id)
    if c is None:
        abort(404)
    c.delete()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_city(state_id):
    """Creates a city"""
    s = storage.get('State', state_id)
    if s is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    if 'name' not in r:
        abort(make_response(jsonify("Missing name"), 400))
    r['state_id'] = state_id
    c = City(**r)
    c.save()
    return make_response(jsonify(c.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """Updates a City at a given ID"""
    c = storage.get('City', city_id)
    if c is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    for k, v in r.items():
        if k not in CITY_IGNORE_KEYS:
            setattr(c, k, v)
    c.save()
    return make_response(jsonify(c.to_dict()), 200)

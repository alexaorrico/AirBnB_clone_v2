#!/usr/bin/python3
"""
Handles all default RESTful API actions for City objects
"""

from . import app_views
from models.city import City
from flask.json import jsonify
from flask import abort
from flask import make_response
from models import storage
from flask import request


@app_views.route("/cities", methods=['GET'])
def cities():
    """Retrieves the list of all City objects"""
    return jsonify([c.to_dict() for c in storage.all('City').values()])


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    """Retrieves a city given its ID"""
    try:
        return jsonify(storage.get('City', city_id).to_dict())
    except AttributeError:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def del_city(city_id):
    """Deletes a city given its ID"""
    try:
        storage.get('City', city_id).delete()
        return make_response(jsonify({}), 200)
    except AttributeError:
        abort(404)


@app_views.route("/cities", methods=['POST'])
def post_city():
    """Creates a city"""
    try:
        r = request.get_json()
        if 'name' not in r:
            abort(make_response(jsonify("Missing name"), 400))
        c = City(**r)
        c.save()
        return make_response(jsonify(c.to_dict()), 200)
    except TypeError:
        abort(make_response(jsonify("Not a JSON"), 400))


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_city(city_id):
    """Updates a City at a given ID"""
    try:
        c = storage.get('City', city_id)
        if c is None:
            abort(404)
        r = request.get_json()
        for key, value in r.items():
            setattr(c, key, value)
    except AttributeError:
        abort(make_response(jsonify("Not a JSON"), 400))
    c.save()
    return make_response(jsonify(c.to_dict()), 200)

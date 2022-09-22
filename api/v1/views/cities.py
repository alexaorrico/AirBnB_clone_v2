#!/usr/bin/python3
"""module to start flask app"""
from multiprocessing.util import ForkAwareThreadLock
from os import stat
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.exceptions import *


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_cityList(state_id):
    """retrieves a list of city objects"""
    try:
        return (jsonify(City.api_get_all(state_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def post_City(state_id):
    """retrieves a list of city objects or creates new city"""
    try:
        return (jsonify(City.api_post(
            request.get_json(silent=True),
            state_id)),
            201)
    except BaseModelInvalidObject:
        abort(404)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelMissingAttribute as attr:
        return (jsonify({'error': 'Missing {}'.format(attr)}), 400)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(City.api_get_single(city_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(City.api_delete(city_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_city_by_id(city_id):
    """retrieves, deletes or updates a city object"""
    try:
        return (jsonify(City.api_put(
                request.get_json(silent=True),
                city_id)), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelInvalidObject:
        abort(404)

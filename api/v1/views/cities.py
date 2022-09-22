#!/usr/bin/python3
"""module to start flask app"""
from multiprocessing.util import ForkAwareThreadLock
from os import stat
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.exceptions import *


# @app_views.route('/states',
#                  methods=['GET'],
#                  strict_slashes=False)
# def get_all_states():
#     """Retrieves the list of all State objects"""
#     return (jsonify(State.api_get_all()), 200)

# @app_views.route('/states',
#                  methods=['POST'],
#                  strict_slashes=False)
# def post_states():
#     """Creates a State"""
#     try:
#         return (jsonify(
#             State.api_post(
#                 request.get_json(silent=True))),
#                 201)
#     except BaseModelMissingAttribute as attr:
#         return (jsonify({'error': 'Missing {}'.format(attr)}), 400)
#     except BaseModelInvalidDataDictionary:
#         return (jsonify({'error': "Not a JSON"}), 400)

# @app_views.route('/states/<string:state_id>',
#                  methods=['GET'],
#                  strict_slashes=False)
# def get_state_by_id(state_id):
#     """handles get State object: state_id"""
#     try:
#         return (jsonify(
#             State.api_get_single(state_id)), 200)
#     except BaseModelInvalidObject:
#         abort(404)

# @app_views.route('/states/<string:state_id>',
#                  methods=['DELETE'],
#                  strict_slashes=False)
# def delete_state_by_id(state_id):
#     """handles State object: state_id"""
#     try:
#         return (jsonify(
#             State.api_delete(state_id)), 200)
#     except BaseModelInvalidObject:
#         abort(404)

# @app_views.route('/states/<string:state_id>',
#                  methods=['PUT'],
#                  strict_slashes=False)
# def put_state_by_id(state_id):
#     """handles update of State object: state_id"""
#     try:
#         return(State.api_put(
#                 request.get_json(silent=True),
#                 state_id),
#                 200)
#     except BaseModelInvalidDataDictionary:
#         return (jsonify({'error': "Not a JSON"}), 400)
#     except BaseModelInvalidObject:
#         abort(404)
    
########### BELOW IS REAL CODE !!!!!!!!!!
########### ABOVE IS GUIDE CODE

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
        returnedValue, code = City.api_post(
            ['name'],
            request.get_json(silent=True),
            state_id)
    except AttributeError:
        abort(404)
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_post_delete_city(city_id):
    """retrieves, deletes or updates a city object"""
    if request.method == 'GET':
        returnedValue, code = City.api_get_single(
            storage.get('City', city_id))
    if request.method == 'DELETE':
        returnedValue, code = City.api_delete(
            storage.get("City", city_id))
    if request.method == 'PUT':
        returnedValue, code = City.api_put(
            ['id', 'state_id', 'created_at', 'updated_at'],
            request.get_json(silent=True),
            storage.get('City', city_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)

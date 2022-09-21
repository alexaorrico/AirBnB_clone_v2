#!/usr/bin/python3
"""module to start flask app"""
from multiprocessing.util import ForkAwareThreadLock
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cityList_createCity():
    """retrieves a list of city objects or creates new city"""
    if request.method == 'GET':
        returnedValue, code = City.api_get_all(
            storage.all("City").values()
        )
    if request.method == 'POST':
        returnedValue, code = City.api_post(
            ['name'], 
            request.get_json(silent=True)
        )
    if code == 404:
        abort(404)
    return (jsonify(returnedValue), code)


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_post_delete_city():
    """retrieves, deletes or updates a city object"""
    if request.method == 'GET':
        returnedValue, code = City.api_get_all(
            storage.get('City', city_id)
        )
    if request.method == 'DELETE':
        returnedValue, code = City.api_delete(
            storage.get("City", city_id)
        )
    if request.method == 'PUT':
        returnedValue, code = City.api_put(
            ['id', 'state_id', 'created_at', 'updated_at'],
            request.get_json(silent=True),
            storage.get('City', city_id)
        )
    if code == 404:
        abort(404)
    storage.save()
    return(jsonify(returnedValue), code)

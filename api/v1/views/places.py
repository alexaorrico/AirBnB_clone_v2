#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models import place
from models.place import Place


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_placeList_createPlace(city_id):
    """retrieves a list of city objects or creates new city"""
    if request.method == 'GET':
        try:
            returnedValue, code = Place.api_get_all(
                storage.get("City", city_id).places)
        except AttributeError as e:
            print(e)
            abort(404)
    if request.method == 'POST':
        try:
            returnedValue, code = Place.api_post(
                ['user_id', 'name'], 
                request.get_json(silent=True),
                city_id)
        except AttributeError as e:
            print(e)
            abort(404)
    if code == 404:
        abort(404)
    return (jsonify(returnedValue), code)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_post_delete_place(place_id):
    """retrieves, deletes or updates a city object"""
    if request.method == 'GET':
        returnedValue, code = Place.api_get_all(
            storage.get('City', place_id))
    if request.method == 'DELETE':
        returnedValue, code = Place.api_delete(
            storage.get("City", place_id))
    if request.method == 'PUT':
        returnedValue, code = Place.api_put(
            ['id','user_id', 'city_id', 'created_at', 'updated_at'],
            request.get_json(silent=True),
            storage.get('City', place_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)


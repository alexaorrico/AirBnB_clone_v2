#!/usr/bin/python3
"""
flask application module for retrieval of
State Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models import amenity
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    print("in correct route")
    if request.method == 'GET':
        returnedValue, code = Amenity.api_get_all(
                    storage.all("Amenity").values()
        )
    if request.method == 'POST':
        print("in POST!")
        returnedValue, code = Amenity.api_post(
                    ["name"],
                    request.get_json(silent=True))
    print(returnedValue)
    print(code)
    return (jsonify(returnedValue), code)


@app_views.route('/states/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """handles Amenity object: amenity_id"""
    if request.method == 'GET':
        returnedValue, code = Amenity.api_get_single(
                        storage.get("Amenity", amenity_id))
    if request.method == 'DELETE':
        returnedValue, code = Amenity.api_delete(
                    storage.get("Amenity", amenity_id))
    if request.method == 'PUT':
        returnedValue, code = Amenity.api_put(
                    ['id', 'created_at', 'updated_at'],
                    request.get_json(silent=True),
                    storage.get("Amenity", amenity_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)

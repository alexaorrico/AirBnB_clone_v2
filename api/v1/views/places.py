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
from models.city import City


# @app_views.route('/places',
#                  methods=['GET', 'POST'],
#                  strict_slashes=False)
# def get_all_places():
#     """Retrieves the list of all Places objects"""
#     if request.method == 'GET':
#         returnedValue, code = Place.api_get_all(
#                     storage.all("Place").values()
#         )
#     if request.method == 'POST':
#         returnedValue, code = Place.api_post(
#                     ["name"],
#                     request.get_json(silent=True))
#     return (jsonify(returnedValue), code)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id):
    """handles Place object: place_id"""
    if request.method == 'GET':
        returnedValue, code = Place.api_get_single(
                        storage.get("Place", place_id))
    if request.method == 'DELETE':
        returnedValue, code = Place.api_delete(
                    storage.get("Place", place_id))
    if request.method == 'PUT':
        returnedValue, code = Place.api_put(
                    ['id', 'user_id', 'created_at', 'updated_at'],
                    request.get_json(silent=True),
                    storage.get("Place", place_id))
    if code == 404:
        abort(404)
    storage.save()
    return (jsonify(returnedValue), code)

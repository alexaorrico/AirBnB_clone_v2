#!/usr/bin/python3
"""
API Place View Module

Defines the API views for the Place objects, providing RESTful
endpoints to interact with Place resources.

HTTP status codes:
- 200: OK: The request has been successfully processed.
- 201: 201 Created: The new resource has been created.
- 400: Bad Request: The server cannot process the request.
- 404: Not Found: The requested resource could not be found on the server.
"""

from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves a list of all Place objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_list = []
    for elem in city.places:
        places_list.append(elem.to_dict())
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates an Place object by its ID """
    if not storage.get(City, city_id):
        abort(404)
    query = request.get_json()
    if not query:
        abort(400, description='Not a JSON')
    if 'user_id' not in query:
        abort(400, description='Missing user_id')
    if not storage.get(User, query['user_id']):
        abort(404)
    if 'name' not in query:
        abort(400, description='Missing name')
    query['city_id'] = city_id
    new = Place(**query)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Gets an Place object by its ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes an Place object by its ID """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates an Place object by its ID """
    if not storage.get(Place, place_id):
        abort(404)
    if request.content_type != 'application/json':
        abort(400, description='Not a JSON')
    place = storage.get(Place, place_id)
    query = request.get_json()
    ignore_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in query.items():
        if key not in ignore_list:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

#!/usr/bin/python3
""" user view """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.base_model import BaseModel


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def get_all_places(city_id):
    """retrieves all place objects for a city"""
    all_cities = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        all_cities.append(place.to_dict())
    return jsonify(all_cities), 200


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Getting individual users by their ids"""
    place = storage.get('Place', place_id)

    if place is None:  # if user_id is not linked to any user obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/place', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """Create a Place, from data provided by the request"""
    city_object = storage.get('City', city_id)
    if city_object is None:  # if the city_id is not linked to any City obj
        abort(404)  # raise a 404 error
    body = request.get_json()  # Flask to transform HTTP request to a dict
    if body is None:  # If the HTTP request body is not valid JSON
        abort(400, {"error": "Not a JSON"})  # raise err and message
    if 'user_id' not in body:  # If the dict doesn't contain the key user_id
        abort(400, {"Missing user_id"})  # raise err
    user_object = storage.get('User', body['user_id'])
    if user_object is not None:  # user_id is not linked to any User object
        abort(404)  # raise err
    if 'name' not in body:  # If the dict doesn't contain the key name
        abort(400, {"Missing name"})
    place_object = Place(city_id=city_id)
    for key, value in body.items():
        setattr(place_object, key, value)
    storage.new(place_object)
    storage.save()
    return jsonify(place_object.to_dict()), 201  # returns new Place


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_by_id(place_id):
    """Updating a place object"""
    body = request.get_json()
    if not body:
        abort(400, {"Not a JSON"})
    place = storage.get('Place', place_id)
    if place is None:  # if place_id is not linked to any User object
        abort(404)
    for key, value in body.items():  # update Place obj with key-val pairs
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200  # return User obj


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deleting a Place object by its id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        del place
    return jsonify({}), 200  # returns an empty dict with status code 200

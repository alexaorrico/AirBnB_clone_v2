#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City
from models.city import City
from models.place import Place

app = Flask(__name__)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id=None):
    """Retrieves the list of all Place objects for a city"""
    cities = storage.all('City')
    city = cities.get('City' + '.' + city_id)
    if city is None:
        abort(404)
    places_list = []
    places = storage.all('Place')
    for place in places.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    """Retrieves a Place object with the id linked to it"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object"""
    obj = storage.get('Place', place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """Creates a Place"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in result:
        return jsonify({"error": "Missing user_id"}), 400
    user_obj = storage.get('User', result['user_id'])
    if user_obj is None:
        abort(404)
    if 'name' not in result:
        return jsonify({"error": "Missing name"}), 400
    place_obj = Place(city_id=city_id)
    for key, value in result.items():
        setattr(place_obj, key, value)
    storage.new(place_obj)
    storage.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """Updates a Place object"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    invalid_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200

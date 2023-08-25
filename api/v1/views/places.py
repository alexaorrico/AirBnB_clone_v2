#!/usr/bin/python3
"""
Create a new view for Places objects that
handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User

app = Flask(__name__)


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_in_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place_in_city(city_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    data['city_id'] = city.id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_by_id(place_id):
    data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

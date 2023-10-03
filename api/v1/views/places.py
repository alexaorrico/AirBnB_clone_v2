#!/usr/bin/python3
"""
The places module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.place import Place

places_bp = Blueprint('places', __name__, url_prefix='/api/v1/places')


@places_bp.route('/', methods=['GET'], strict_slashes=False)
def get_places():
    places = [place.to_dict() for place in storage.all(Place).values()]
    return jsonify(places)


@places_bp.route('/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@places_bp.route('/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@places_bp.route('/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@places_bp.route('/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'name' not in data:
        abort(400, description='Missing name')
    user_id = data['user_id']
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@places_bp.route('/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())

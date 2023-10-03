#!/usr/bin/python3
"""
The placess module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.place import Place

places_bp = Blueprint('placess', __name__, url_prefix='/api/v1/places')


@places_bp.route('/', methods=['GET'], strict_slashes=False)
def get_placess():
    placess = [places.to_dict() for places in storage.all(Place).values()]
    return jsonify(placess)


@places_bp.route('/<places_id>', methods=['GET'], strict_slashes=False)
def get_places(places_id):
    places = storage.get(Place, places_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict())


@places_bp.route('/<places_id>', methods=['DELETE'], strict_slashes=False)
def delete_places(places_id):
    places = storage.get(Place, places_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({})


@places_bp.route('/', methods=['POST'], strict_slashes=False)
def create_places():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_places = Place(**data)
    new_places.save()
    return jsonify(new_places.to_dict()), 201


@places_bp.route('/<places_id>', methods=['PUT'], strict_slashes=False)
def update_places(places_id):
    places = storage.get(Place, places_id)
    if places is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'city_id', 'created_at', 'updated_at']:
            setattr(places, key, value)
    places.save()
    return jsonify(places.to_dict())

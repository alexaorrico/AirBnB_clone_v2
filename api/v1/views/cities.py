#!/usr/bin/python3
"""
The citiess module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.city import City

cities_bp = Blueprint('citiess', __name__, url_prefix='/api/v1/cities')


@cities_bp.route('/', methods=['GET'], strict_slashes=False)
def get_citiess():
    citiess = [cities.to_dict() for cities in storage.all(City).values()]
    return jsonify(citiess)


@cities_bp.route('/<cities_id>', methods=['GET'], strict_slashes=False)
def get_cities(cities_id):
    cities = storage.get(City, cities_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@cities_bp.route('/<cities_id>', methods=['DELETE'], strict_slashes=False)
def delete_cities(cities_id):
    cities = storage.get(City, cities_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()
    return jsonify({})


@cities_bp.route('/', methods=['POST'], strict_slashes=False)
def create_cities():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_cities = City(**data)
    new_cities.save()
    return jsonify(new_cities.to_dict()), 201


@cities_bp.route('/<cities_id>', methods=['PUT'], strict_slashes=False)
def update_cities(cities_id):
    cities = storage.get(City, cities_id)
    if cities is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(cities, key, value)
    cities.save()
    return jsonify(cities.to_dict())

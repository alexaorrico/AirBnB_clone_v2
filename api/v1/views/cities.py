#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from modles import storage
from models.city import City
from api.vi.views import app_views


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Retreive the list of all citys objects"""
    cities = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slasheds=False)
def get_city(city_id):
    """Retrieve the specific city object by Id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slasheds=False)
def delete_city(city_id):
    """Delete a City object by ID"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities', methods=['POST'], strict_slasheds=False)
def create_city():
    """Create a new city object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/citys/<city_id>', methods=['PUT'], strict_slasheds=False)
def update_city(city_id):
    """Update a City Object by ID"""
    if city:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)


        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)

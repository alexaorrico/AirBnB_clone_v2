#!/usr/bin/python3
"""
this module is to return cities objects
"""
from flask import jsonify, request, abort
from models.city import City


def to_dict(city):
    """Converts a City object to a dictionary."""
    return city.to_dict()


def create_city(state_id):
    """Creates a new City."""
    state = State.get_by_id(state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    new_city = City(state_id=state_id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


def get_all_cities(state_id):
    """Retrieves the list of all City objects of a State."""
    state = State.get_by_id(state_id)
    if not state:
        abort(404)

    cities = City.get_all_by_state(state_id)
    return jsonify({'cities': [to_dict(city) for city in cities]})


def get_city(city_id):
    """Retrieves a City object by ID."""
    city = City.get_by_id(city_id)
    if not city:
        abort(404)
    return jsonify(to_dict(city))


def delete_city(city_id):
    """Deletes a City object by ID."""
    city = City.get_by_id(city_id)
    if not city:
        abort(404)

    city.delete()
    return jsonify({}), 200


def update_city(city_id):
    """Updates a City object by ID."""
    city = City.get_by_id(city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(to_dict(city)), 200

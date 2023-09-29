#!/usr/bin/python3
"""API endpoints for cities"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City


def get_obj_or_abort(obj_cls, obj_id):
    """Retrieve a State object by ID or abort with 404 if not found"""
    obj = storage.get(obj_cls, obj_id)
    if obj is None:
        abort(404)
    return obj


def create_city(data, state_id):
    """Create a new state in the database."""
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return new_city


def validate_json():
    """Validate that the request data is in JSON format."""
    try:
        return request.get_json()
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(state_id=None):
    """Route for manipulating City objects"""

    if request.method == 'GET':
        # Get a list of all City object for a state
        state = get_obj_or_abort('State', state_id)
        cities_list = [city.to_dict() for city in state.cities]
        return jsonify(cities_list)

    if request.method == 'POST':
        # Add a State to the list
        get_obj_or_abort('State', state_id)
        data = validate_json()
        if "name" not in data:
            abort(400, "Missing name")
        new_city = create_city(data, state_id)
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def city_with_id(city_id=None):
    """Route for manipulating a specific City object"""

    city = get_obj_or_abort('City', city_id)

    if request.method == 'GET':
        # Get a specific state by id
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        # Delete a specific state by id
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific state by id
        data = validate_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)

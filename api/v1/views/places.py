#!/usr/bin/python3
"""API endpoints for places"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


def get_obj_or_abort(obj_cls, obj_id):
    """Retrieve an object by ID or abort with 404 if not found"""
    obj = storage.get(obj_cls, obj_id)
    if obj is None:
        abort(404)
    return obj


def create_place(data, city_id):
    """Create a new city in the database."""
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return new_place


def validate_json():
    """Validate that the request data is in JSON format."""
    try:
        return request.get_json()
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_by_city(city_id=None):
    """Route for retrieving Review objects"""

    if request.method == 'GET':
        # Get a list of all Place object for a city
        city = get_obj_or_abort('City', city_id)
        places_list = [place.to_dict() for place in city.places]
        return jsonify(places_list)

    if request.method == 'POST':
        # Add a Place object to the list
        get_obj_or_abort('City', city_id)
        data = validate_json()
        if "user_id" not in data:
            abort(400, "Missing user_id")
        get_obj_or_abort('User', data['user_id'])
        if "name" not in data:
            abort(400, "Missing name")
        new_place = create_place(data, city_id)
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def place_with_id(place_id=None):
    """Route for retrieving a specific Place object"""

    place = get_obj_or_abort('Place', place_id)

    if request.method == 'GET':
        # Get a specific place by id
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        # Delete a specific place by id
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific place by id
        data = validate_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at",
                           "city_id", "user_id"]:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)

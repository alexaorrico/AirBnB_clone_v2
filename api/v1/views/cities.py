#!/usr/bin/python3
"""View of Cities for RESTFul API"""

from api.v1.views import app_views, validate_model, get_json
from flask import jsonify
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = validate_model("State", state_id)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = validate_model("City", city_id)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = validate_model("City", city_id)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    validate_model("State", state_id)
    body = get_json(['name'])
    body["state_id"] = state_id
    city = City(**body)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = validate_model("City", city_id)
    body = get_json()
    for key, value in body.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

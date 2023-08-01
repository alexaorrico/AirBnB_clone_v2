#!/usr/bin/python3
"""City view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.city import City
from models.state import State


# Route to get cities
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Return a JSON reponse of all city objects specified by state id
    """

    # Get list of city objects dictionary by state_id
    city_objs = [city.to_dict() for city in storage.all(
        City).values() if city.state_id == state_id]

    if len(city_objs) == 0:
        abort(404)
    return jsonify(city_objs)

# Route to get a city object


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Return a JSON reponse of a city object specified by city id
    """

    # Get dictionary of state object by id
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


# Route to delete a city object


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city object specified by it id"""

    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

# Route to create a city object


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a new city object"""
    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in content:
        abort(400, 'Missing name')  # raise bad request error
    city = City(**content)
    city.save()

    return jsonify(city.to_dict()), 201

# Route to update a city object


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a city object specified by id"""

    city = storage.get(City, city_id)  # Get city by id

    if city is None:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)  # Update city with new data
            city.save()

    return jsonify(city.to_dict()), 200

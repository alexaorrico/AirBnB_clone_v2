#!/usr/bin/python3
""" CRUD operation on state object"""
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort, request, make_response



@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    The function `all_states` retrieves all instances of the
    `State` class from storage and returns them as a JSON list."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(city_id):
    """
    The function `states_id` takes an ID as input and returns the
    corresponding state object as a JSON response, or raises a
    404 error if the state is not found.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_id_delete(city_id):
    """
    The function `states_id_delete` deletes a state
    object from storage based on its ID.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def city_post():
    """
    The function `states_post()` receives a JSON object,
    checks if it is valid, creates a new State object,
    saves it to storage, and returns the State object as a JSON response.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """
    The function updates the attributes of a state object based
    on the provided JSON data and returns the updated state
    object as a JSON response."""
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setatte(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)

"""@app_views.errorhandler(404)
def not_found(error):
    ""not found""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response"""

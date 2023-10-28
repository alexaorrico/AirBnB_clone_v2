#!/usr/bin/python3
"""create a new view for City objects that handles
all default RESTFul API actions"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieve a list of all City objects of a State.

    Returns:
        JSON response: A JSON response containing a list of all City objects
        of a State.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieve a City object.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        JSON response: A JSON response containing a City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a City object.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        JSON response: An empty JSON response.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Create a City object.

    Returns:
        JSON response: A JSON response containing a new City object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    kwargs = request.get_json()
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    Update a City object.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        JSON response: A JSON response containing an updated City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)


if __name__ == '__main__':
    pass

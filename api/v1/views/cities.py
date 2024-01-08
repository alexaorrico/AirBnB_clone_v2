#!/usr/bin/python3
"""State view"""
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/cities', strict_slashes=False)
def get_cities():
    """Retrieves the list of all cities objects"""
    from models import storage
    from models.city import City
    cities = storage.all(City)
    cities_list = []
    for city in cities.values():
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all cities objects"""
    from models import storage
    from models.state import State
    cities_list = []
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    from models import storage
    from models.city import City
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    from models import storage
    from models.city import City
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a city"""
    from models import storage
    from models.state import State
    from models.state import City
    from flask import request
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400

    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    city = City(**request.get_json())
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a city object"""
    from models import storage
    from models.city import City
    from flask import request
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

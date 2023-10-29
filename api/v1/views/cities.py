from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    retrieves all City objects in a specific State
    """
    state = storage.get(State, state_id)
    if state:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    retrieves a City object
    """
    city = storage.get(City, city_id)
    if city:
        response = city.to_dict()
        return jsonify(response)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    deletes a City object
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    create a City object
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')

    city = City(name=data['name'], state_id=state_id)
    city.save()
    response = city.to_dict()
    return jsonify(response), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    updates a city object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignore_attributes = ['id', 'state_id', 'created_at', 'updated_at']
    for attribute, value in data.items():
        if attribute not in ignore_attributes:
            setattr(city, attribute, value)
    city.save()
    response = city.to_dict()
    return jsonify(response), 200

from flask import request, jsonify, abort
from api.v1.views import app_views
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities]), 200

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

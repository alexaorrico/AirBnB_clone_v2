from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
    )
def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="Not found")
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="Not found")
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="Not found")
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
    )
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="Not found")
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404, description="Not found")
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

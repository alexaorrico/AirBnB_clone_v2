i!/usr/bin/python3
""" City objects handles all default RESTFul API"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description="Not found")
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object. : GET /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())        


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities_id(city_id):
    """Deletes a City object: DELETE /api/v1/cities/<city_id>"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="Not found")
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'])
def post_cities(state_id):
    """Creates a City: POST /api/v1/states/<state_id>/cities"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="Not found")
    new_city = City(**request.get_json())
    new_city.state_id = state.id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_cities(city_id):
    """Updates a City object: PUT /api/v1/cities/<city_id>"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(City, city_id):
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'create_at', 'update_at']:
            cities = storage.get(City, city_id)
            setattr(cities, key, value)
        storage.save()
        return make_response(jsonify(cities.to_dict()), 200)

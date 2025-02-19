#!/usr/bin/python3
"""States API"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<states_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """Retrieve cities given state IDs"""
    # iterate thru storage.all() 
    # if cls is City
    # if state_id == state_id
    # return city.to_dict()
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """Retrieve city Using city ID"""
    data = storage.get(City, city_id)
    if not data:
        abort(404)
    return jsonify(data.to_dict()), 200

@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete city with id"""
    data = storage.get(City, city_id)
    if not data:
        abort(404)
    else:
        storage.delete(data)
        storage.save()
    return jsonify({}), 200

# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def post_states():
#     """ Post State """
#     if not request.is_json:
#         return jsonify('Not a JSON')

#     data = request.get_json()
    
#     if 'name' not in data:
#         abort(404, 'Missing name')

#     inst = State(**data)
#     inst.save()

#     return jsonify(inst.to_dict()), 201    

@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    """update city information give state ID"""

    city = storage.get(City, city_id)

    if not city:
        abrot(404)

    if not request.is_json:
        abort(404, "Not a JSON")

    data = request.get_json()

    # if 'name' not in data:
    #     abort(404, "Missing name data")

    ignore_fields = ['id', 'updated_at', 'created_at']

    for key, value in data.items():
        if key not in ignore_fields:
            setattr(state, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200

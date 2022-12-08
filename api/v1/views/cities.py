#!/usr/bin/python3
"""
New view for class State
To handle all default Restful API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities_by_state(state_id):
    """Returns the list of all cities"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    cities_list = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def pick_city_obj(city_id):
    """Retrieves a `City` object/Error if no linkage to any id"""
    city_pick = storage.get("City", city_id)
    if city_pick is None:
        # use abort to return 404
        # in the middle of a route
        abort(404)
    return jsonify(city_pick.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a `City` object based on its id
    Raise error if no linkage found
    """
    city_rm = storage.get("City", city_id)
    if city_rm is None:
        abort(404)
    city_rm.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def post_city(state_id):
    """Method to create a `City` object"""
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    elif 'name' not in json_data:
        abort(400, 'Missing name')
    all_states = storage.get("State", state_id)
    if all_states is None:
        abort(404)
    json_data['state_id'] = state_id
    new_post = City(**json_data)
    new_post.save()
    return jsonify(new_post.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def upd_city(city_id):
    """
    Update a `City` object
    Error if no linkage found
    """
    # second requirement comes first
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')

    city_obj = storage.get("City", city_id)
    # gather City object matching the city_id provided
    if city_obj is None:
        # means no City are linked to city_id provided
        abort(404)
    city_obj.name = json_data['name']
    # ignore all other keys(id, state_id, created_at....)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200

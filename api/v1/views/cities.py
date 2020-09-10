#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ Retrieves a list with all citiy objects of a State. """
    city_objs = storage.all(City).values()
    list_dic_city = []
    for city in city_objs:
        if city.state_id == state_id:
            list_dic_city.append(city.to_dict())
    if len(list_dic_city) == 0:
        abort(404)
    return jsonify(list_dic_city)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def all_states_N():
    """ Retrieves a list with all state, including the new one. """
    body_dic = request.get_json()
    if "name" not in body_dic:
        return jsonify({'error': 'Missing name'}), 400
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    new_state = State(**body_dic)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a current state"""
    state_obj = storage.get(State, state_id)
    if state_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at']
            if key not in ignore_keys:
                setattr(state_obj, key, value)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete current state """
    state_obj = storage.get(State, state_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get current state """
    state_obj = storage.get(State, state_id)
    if state_obj:
        return jsonify(state_obj.to_dict())
    else:
        abort(404)

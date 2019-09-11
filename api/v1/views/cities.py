#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id=None):
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found 1')

    cities = storage.all('City')
    city_list = []
    for val in cities.values():
        if val.state_id == state_id:
            city_list.append(val.to_dict())

    if len(city_list) == 0:
        abort(404, 'Not found 2')

    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    ''' returns an individual state object '''
    obj = storage.get('City', city_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')
    obj = obj.to_dict()
    return jsonify(obj)





"""
@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_all_states():
    data = storage.all(State)
    new = [val.to_dict() for key, val in data.items()]
    return jsonify(new)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    ''' deletes an individual state '''
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')

    obj.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    ''' updates an individual state '''
    obj = storage.get(State, state_id)
    if obj is None:
        ''' if no state obj with that id '''
        abort(404, 'Not found')
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in args.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200

@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    ''' create a state if doesn't already exist '''
    args = request.get_json()
    if not args:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in args:
        return jsonify({"error": "Missing name"}), 400
    obj = State(**args)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
"""

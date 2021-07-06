#!/usr/bin/python3
<<<<<<< HEAD
"""Flask application that handle cities API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
# from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Return list of cities in a state"""
    states_all = storage.all("State")
    try:
        unique_state = states_all["{}.{}".format("State",
                                                 state_id)]
        city_list = []
        for city in unique_state.cities:
            city_list.append(city.to_dict())
    except KeyError:
        abort(404)
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_cities_id(city_id):
    """Return a single city"""
    if request.method == 'GET':
        cities_all = storage.all("City")
        try:
            unique_city = cities_all["{}.{}".format("City",
                                                    city_id)]
        except KeyError:
            abort(404)
        return jsonify(unique_city.to_dict())
    elif request.method == 'DELETE':
        obj_to_delete = storage.get("City", city_id)
        if obj_to_delete is None:
            abort(404)
        else:
            storage.delete(obj_to_delete)
            storage.save()
            return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Post new city"""
    json_tmp = request.get_json()
    if not json_tmp:
        return jsonify("Not a JSON"), 400
    try:
        json_tmp['name']
    except (KeyError, TypeError):
        return jsonify("Missing name"), 400
    all_states = storage.all("State")
    try:
        all_states["{}.{}".format("State", state_id)]
        new_city = City(**json_tmp, state_id=state_id)
        storage.new(new_city)
        storage.save()
        return(jsonify(new_city.to_dict())), 201
    except KeyError:
        abort(404)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Put method to update city"""
    cities_all = storage.all("City")
    try:
        unique_city = cities_all["{}.{}".format("City", city_id)]
        json_tmp = request.get_json()
        if not json_tmp:
            return jsonify("Not a JSON"), 400
        for key, value in json_tmp.items():
            if key == 'id' or key == 'updated_at' or key == 'created_at':
                pass
            setattr(unique_city, key, value)
        unique_city.save()
    except KeyError:
        abort(404)
    return jsonify(unique_city.to_dict()), 200
=======
""" Flask application that handle cities API"""
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Return list of cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        city_dict = city.to_dict()
        cities_list.append(city_dict)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve a single city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'name' not in json_obj:
        return jsonify("Missing name"), 400
    json_obj['state_id'] = state_id
    new_city = City(**json_obj)
    new_city.save()
    city = new_city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """Put a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "update_at", "created_at", "state_id"]
    for key, value in json_obj.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    new_city = city.to_dict()
    return jsonify(new_city), 200
>>>>>>> 4ea20951bb01e71fab223152c944e95ad3e49dc1

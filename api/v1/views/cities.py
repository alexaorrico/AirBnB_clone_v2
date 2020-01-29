#!/usr/bin/python3
"""Flask application that handle states API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
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
    new_city = City(**json_tmp, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return(jsonify(new_city.to_dict())), 201


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

#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def all_city_by_id(state_id):
    """return json"""
    city_list = []
    state = storage.get(State, user_id)
    if state is None:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'], strict_slashes=False)
def all_city(city_id):
    """return json"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city_by_id(city_id):
    """return json"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities", methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """return json"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = request.get_json()
    st = City(**state)
    st.state_id = state_id
    st.save()
    return make_response(jsonify(st.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city_by_id(city_id):
    """return json"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

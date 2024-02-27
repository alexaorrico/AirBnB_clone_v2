#!/usr/bin/python3
""" City objects that handles all default RESTFul API actions """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, make_response, request
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/states/<citie_id>', methods=['GET'], strict_slashes=False)
def get_state(citie_id):
    state = storage.get(State, citie_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/cities/<citie_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_citie(citie_id):
    citie = storage.get("City", citie_id)
    if not citie:
        abort(404)
    citie.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_citie(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    new_citie = request.get_json()
    if not new_citie:
        abort(400, "Not a JSON")
    if "name" not in new_citie:
        abort(400, "Missing name")
    city = City(**new_citie)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<citie_id>', methods=['PUT'],
                 strict_slashes=False)
def put_citie(citie_id):
    citie = storage.get("City", citie_id)
    if not citie:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    for key, v in body_request.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(citie, key, v)
    storage.save()
    return make_response(jsonify(citie.to_dict()), 200)

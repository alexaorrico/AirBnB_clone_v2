#!/usr/bin/python3
""" City view """
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<string:id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(id):
    """ get all instances of city linkedto a state"""
    if request.method == 'GET':
        state = storage.get(State, id)
        cities = storage.all(City)
        if state is None:
            abort(404)
        values = []
        for value in cities.values():
            if value.state_id == state.id:
                values.append(value.to_dict())
        return jsonify(values)


@app_views.route('cities/<string:id>', methods=['GET'],
                 strict_slashes=False)
def get_city(id):
    """ get an instance of city """
    if request.method == 'GET':
        city = storage.get(City, id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())


@app_views.route('cities/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(id):
    """delete an instance of city class"""
    if request.method == 'DELETE':
        city = storage.get(City, id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('states/<string:id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city_linked_to_state(id):
    """add an instance of city linked to a state_id"""
    if request.method == 'POST':
        state = storage.get(State, id)
        if state is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        if "name" not in body:
            return make_response(jsonify({"error": "Missing name"}), 400)
        setattr(body, "state_id", id)
        new_city = City(**body)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<string:id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(id):
    """ update an instatnce of city """
    if request.method == 'PUT':
        city = storage.get(City, id)
        if city is None:
            abort(404)
        if not request.get_json():
            return make_respone(jsonify({"error": "Not a JSON"}), 400)
        body = request.get_json()
        for k, v in body.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)

#!/usr/bin/python3
""" Handle RESTful API actions for City objects """
from api.v1.views import app_views
from flask import abort, request, jsonify, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_city_objects(state_id):
    """ Return cities for a given state object """
    try:
        state_obj = storage.get(State, state_id)
        state_cities = [c.to_dict() for c in state_obj.cities]
        return jsonify(state_cities)
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_objects(city_id):
    """ Retrieves the list of all City objects """
    city_obj = storage.get(City, city_id)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_object(city_id):
    """ Delete a City object """
    try:
        city_obj = storage.get(City, city_id)
        storage.delete(city_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    except:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_object(state_id):
    """ Create a new City object """
    if not request.get_json():
        abort(400, description='Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, description='Missing name')
    else:
        try:
            state_obj = storage.get(State, state_id)
        except:
            abort(404)

        content = request.get_json()
        city = City()
        city.name = content['name']
        city.state_id = state_id
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_object(city_id):
    """ Update the attributes of a State object """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    content = request.get_json()
    nope = ['id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in nope:
            setattr(city_obj, key, value)
    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 200)

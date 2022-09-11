#!/usr/bin/python3
"""variable app_views which is an instance of Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities_state(state_id=None):
    """Retrieves the list of all City objects of a State"""
    states = storage.all('State')
    states = "state.{}".format(states.get(state_id))
    if states is not None:
        city = storage.all("City")
        city_list = []
        for value in city.values():
            print(value.id)
            if value.id == state_id:
                city_list.append(value.to_dict())
                return jsonify(city_list)
        abort(404)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def _cities(city_id=None):
    """Retrieves a City object GET"""
    city = storage.all("City")
    city_list = []
    for value in city.values():
        if value.id == city_id:
            city_list.append(value.to_dict())
            return jsonify(city_list)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete(city_id=None):
    """Deletes a City object: DELETE"""
    if city_id is not None:
        city = storage.get(City, city_id)
        if state is not None:
            storage.delete(city)
            storage.save()
            return {}, 200
        else:
            abort(404)
    abort(404)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def _post(state_id=None):
    """ Creates a City: POST """
    states = storage.all('State')
    states = "state.{}".format(states.get(state_id))
    if states is None:
        abort(404)
    response = request.get_json()
    if type(response) is dict:
        if 'name' in response:
            new_city = State(**response)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
        else:
            abort(400, description="Missing name")
    else:
        abort(400, description="Not a JSON")
    return new_city


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def _put(city_id=None):
    """ Updates a City object: PUT """
    response = request.get_json()
    if type(response) is dict:
        city = storage.get(City, city_id)
        if city is not None:
            response.pop("id", None)
            response.pop("created_at", None)
            response.pop("updated_at", None)
            for key, value in response.items():
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
        else:
            abort(404)
    else:
        abort(400, description="Not a JSON")

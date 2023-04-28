#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """retrieve the list of all City objects"""
    # retrieve states and IDs registered in the State class
    state = storage.get(State, state_id)
    # raise an error if the state_id is not linked to any State object
    if state is None:
        abort(404)
    else:
        cities = storage.all(City).values()
        list_cities = [city.to_dict() for city in state.cities]
        return jsonify(list_cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieve a City object"""
    # retrieve City objects and their IDs registered in the City class
    city = storage.get(City, city_id)

    # raise an error if the city_id is not linked to any City object
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a City object"""
    # retrieve all City objects registered in the City class
    city = storage.get(City, city_id)

    # raise an error if the city_id doesn't match
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    # return an empty dictionary with the status code 200
    return (jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a city object"""
    # get State object which is linked to the state_id
    state = storage.get(State, state_id)
    # raise an error if the state_id is not linked to any State object
    if state is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    # raise error if the dictionary doesn’t contain the key name
    if 'name' not in body:
        abort(400, 'Missing name')

    body['state_id'] = state_id
    city = City(**body)
    storage.new(city)
    city.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a City object"""
    # get a City object and its ID
    city = storage.get(City, city_id)
    # raise error id city_id is not linked to any City object
    if city is None:
        abort(404)

    # transform the HTTP body request to a dictionary
    body = request.get_json()
    # raise error if the the HTTP body request is not a valid JSON
    if body is None:
        abort(400, 'Not a JSON')

    ignore_key = ['id', 'state_at', 'created_at' 'updated_at']
    for key, value in body.items():
        if key not in ignore_key:
            setattr(city, key, value)

    storage.save()
    return (jsonify(city.to_dict()), 200)

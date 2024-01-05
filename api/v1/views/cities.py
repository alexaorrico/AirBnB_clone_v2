#!/usr/bin/python3
""" City Object View module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Obtain every city object in a given state.
    args:
        state_id: The state for which all cities should be displayed
    return:
        Every urban item in json
    """
    state = storage.get(State, state_id)

    if state:
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    method to use get verb to obtain city instance by id
    args:
        city_id: The type of city we desire
    return:
        instance 404 of a city
    """
    city = storage.get(City, city_id)

    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    remove the city instance using id and remove verb
    arg:
        city_id: The city ID that we wish to remove
    return:
        the dictionary is empty and status 200.
    """
    city = storage.get(City, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    create a fresh city object
    args:
        state_id:
            state identity of the city
    return:
        201 status and a new city item
    """
    state = storage.get(State, state_id)

    if state:
        if not request.get_json():
            return (jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return (jsonify({'error': 'Missing name'}), 400)
        new_city = request.get_json().get('name')
        city_object = City(name=new_city, state_id=state_id)
        city_object.save()
        return (jsonify(city_object.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    update city instance using a PUT verb request and city_id.

    args:
        city_id: The city ID that we wish to update
    return:
        city item having 200 ok status
    """
    city = storage.get(City, city_id)

    if city:
        if not request.get_json():
            return (jsonify({'error': 'Not a JSON'}), 400)
        for k, v in request.get_json().items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict())
    else:
        abort(404)

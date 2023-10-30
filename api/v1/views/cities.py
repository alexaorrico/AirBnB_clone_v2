#!/usr/bin/python3
""" module for city object view"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    get all city objects for a certain state.
    args:
        state_id: state for which we want to see all cities
    return:
        each city object as json
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
    function to get city instance by id using get verb
    args:
        city_id: id of city we want
    return:
        city instance, else 404
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
    delete city instance with id, using delete verb
    arg:
        city_id: id of city we want to delete
    return:
        ok status (200) and empty dictionary
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
    make a new city object
    args:
        state_id:
            id of state where city is
    return:
        new city object and 201 status
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
    update city instance by city_id with a PUT verb request.

    args:
        city_id: id of city we want to update
    return:
        city object with ok status(200)
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

#!/usr/bin/python3
"""restful actions for cities"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request

@app_views.route('/api/v1/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_cities_from_state(id):
    """gets cities from state based on state id"""
    city_list = []
    get_state = storage.get(State, id)
    if get_state is None:
        abort(404)
    else:
        for city in get_state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)


@app_views.route('/api/v1/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def get_city(id):
    """retrieves a city by id"""
    get_city = storage.get(City, id)
    if get_city is None:
        abort(404)
    else:
        return jsonify(get_city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def del_city(id):
    """deletes a city by id"""
    empty_dict = {}
    get_city = storage.get(City, id)
    if get_city is None:
        abort(404)
    else:
        storage.delete(get_city)
        storage.save()
        return empty_dict, 200


@app_views.route('/api/v1/states/<state_id>/cities', methods["POST"],
                 strict_slashes=False)
def create_city(id):
    """creates a city object from state id"""
    city_json = request.get()
    get_state = storage.get(State, id)
    if get_state is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'name' not in city_json:
        abort(400, description="Missing name")
    else:
        ###########################################
        ###########################################
        # how to actually create new city object? #
        ###########################################
        ###########################################
        return 201


@app_view.route('/api/v1/cities/<city_id>', methods=["PUT"],
                strict_slashes=False)
def update_city(id):
    """updates a city object"""
    city_json = request.get_json
    get_city = storage.get(City, id)
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    if get_city is None:
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    else:
        for key, value in city_json.items:
            if key not in ignored_keys:
                setattr(get_city, key, value)
            storage.save()
        return jsonify(get_city.to_dict()), 200

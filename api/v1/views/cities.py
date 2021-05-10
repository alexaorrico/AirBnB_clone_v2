#!/usr/bin/python3
"""states route handler"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


def check(obj, city_id):
    """
        checking if city valid and linked to state in storage
    """
    try:
        checker = storage.get(obj, city_id)
        checker.to_dict()
    except Exception:
        abort(404)
    return checker


def get_all(state_id, city_id):
    """
       Retrieves the list of all City objects
       from  state
    """
    if (city_id is not None):
        get_city = check(City, city_id).to_dict()
        return jsonify(get_city)
    my_state = storage.get(State, state_id)
    try:
        all_cities = my_state.cities
    except Exception:
        abort(404)
    cities = []
    for c in all_cities:
        cities.append(c.to_dict())
    return jsonify(cities)


def delete_city(id_city):
    """
        deleting a state request
    """
    city = check(City, id_city)
    storage.delete(city)
    storage.save()
    response = {}
    return jsonify(response)


def create_city(request, state_id):
    """
        Create new state request
    """
    check(State, state_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, 'Not a JSON')
    try:
        name_city = request_json['name']
    except Exception:
        abort(400, "Missing name")
    city = City(name=name_city, state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict())


def do_update_city(city_id, request):
    """
        Updates a City object
    """
    get_city = check(City, city_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_city, k, v)
    storage.save()
    return jsonify(get_city.to_dict())


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'],
                 defaults={'city_id': None}, strict_slashes=False)
@app_views.route('/cities/<city_id>', defaults={'state_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def cities(state_id, city_id):
    """
        Handle cities requests
    """
    if (request.method == "GET"):
        return get_all(state_id, city_id)
    elif (request.method == "DELETE"):
        return delete_city(city_id)
    elif (request.method == "POST"):
        return create_city(request, state_id), 201
    elif (request.method == "PUT"):
        return do_update_city(city_id, request), 200

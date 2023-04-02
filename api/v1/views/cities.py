#!/usr/bin/python3
""" handles all default RestFul API """


from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def cities_view(state_id):
    """ return a jsonified cities objects """
    get_id = storage.get(State, state_id)
    if get_id is None:
        abort(404)
    obj_cities_list = get_id.cities  # grab city objs of the state passed in
    cities_list_to_dict = []
    for value in obj_cities_list:
        cities_list_to_dict.append(value.to_dict())
    return (jsonify(cities_list_to_dict))


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def cities_id_view(city_id):
    """ returns a jsonified city obj by city_id """
    get_id = storage.get(City, city_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete city obj by city_id """
    get_id = storage.get(City, city_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ creating a city object """
    get_id = storage.get(State, state_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "name" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    data_req['state_id'] = state_id
    # ^ set state_id key of city obj's dict equal to value of state_id
    # that was passed into the method
    new_city_obj = City(**data_req)
    new_city_obj.save()
    return (jsonify(new_city_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ updating a city object """
    get_id = storage.get(City, city_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at", "state_id"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()
    return (jsonify(get_id.to_dict()), 200)

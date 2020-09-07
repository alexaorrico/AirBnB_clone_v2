#!/usr/bin/python3
"""
Cities file
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def jsonify_city_1(state_id):
    """ Function that returns a JSON """
    the_obj = storage.get(State, state_id)
    if the_obj is None:
        abort(404)
    my_list = []
    for obj in the_obj.cities:
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def jsonify_city_2(city_id):
    """Function Retrieves a City object"""
    the_obj = storage.get(City, city_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def jsonify_city_3(city_id):
    """Function delete a City Object"""
    the_obj = storage.get(City, city_id)
    if the_obj is None:
        abort(404)
    storage.delete(the_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def jsonify_city_4(state_id):
    json_post = request.get_json()
    the_obj = storage.get(State, state_id)
    if the_obj is None:
        abort(404)
    if not json_post:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in json_post:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    json_post['state_id'] = state_id
    new = City(**json_post)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def jsonify_city_5(city_id):
    the_obj = storage.get(City, city_id)
    json_put = request.get_json()
    if the_obj is None:
        abort(404)
    if not json_put:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_put.items():
        if key not in ['id', 'state_id', 'created_at', 'update_at']:
            setattr(the_obj, key, value)
    storage.save()
    return make_response(jsonify(the_obj.to_dict()), 200)

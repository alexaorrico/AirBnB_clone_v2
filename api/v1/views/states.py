#!/usr/bin/python3
"""
States file
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def jsonify_app_1():
    """ Function that returns a JSON """
    the_objects = storage.all(State)
    my_list = []
    for key, obj in the_objects.items():
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def jsonify_app_2(state_id):
    """ Function that returns a the state id JSON """
    the_obj = storage.get(State, state_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def jsonify_app_3(state_id):
    """ Function that Deletes a State object  JSON """
    the_obj = storage.get(State, state_id)
    if the_obj is None:
        abort(404)
    storage.delete(the_obj)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def jsonify_app_4():
    """Creates a State"""
    json_post = request.get_json()
    if not json_post:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in json_post:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new = State(**json_post)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def jsonify_app_5(state_id):
    """Updates a State object: PUT"""
    the_obj = storage.get(State, state_id)
    json_put = request.get_json()
    if the_obj is None:
        abort(404)
    if not json_put:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_put.items():
        setattr(the_obj, key, value)
    storage.save()
    return make_response(jsonify(the_obj.to_dict()), 200)

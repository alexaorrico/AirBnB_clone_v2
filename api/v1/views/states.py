#!/usr/bin/python3
""" functions GET, PUT, POST & DELETE """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_all():
    """ get all the states """
    state = []
    all_states = storage.all(State)
    for i in all_states:
        state.append(all_states[i].to_dict())
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_id(state_id):
    """ get status by id """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict()), 200
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def del_id(state_id):
    """ delete state by id """
    state = storage.get(State, state_id)
    storage.delete(state)
    storage.save()
    if not state:
        abort(404)
    return ({}), 200


@app_views.route('/states', methods=['POST'])
def add():
    """ add statte to storage """
    if request.json:
        content = request.get_json()
        if "name" not in content.keys():
            return jsonify("Missing name"), 400
        else:
            add_state = State(**content)
            add_state.save()
            return jsonify(add_state.to_dict()), 201
    return jsonify("Not a JSON"), 400


@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id):
    """ update states with id """
    dic = storage.all(State)
    for i in dic:
        if dic[i].id == state_id:
            if request.json:
                ignore = ["id", "update_at", "created_at"]
                content = request.get_json()
                for items in content:
                    if items not in ignore:
                        setattr(dic[i], items, content[items])
                dic[i].save()
                return jsonify(dic[i].to_dict())
            else:
                return jsonify("Not a JSON"), 400
    abort(404)

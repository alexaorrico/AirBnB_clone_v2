#!/usr/bin/python3
""" States view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ all State objects """
    return (jsonify([state.to_dict() for state in storage.all(
            "State").values()]))


@app_views.route('/states', strict_slashes=False, methods=['POST'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=[
                 'GET', 'DELETE', 'POST', 'PUT'])
def a_state(state_id=None):
    """ retrieves a State object by id """

    if state_id:
        try:
            obj = storage.all("State").pop("State." + state_id)
        except KeyError:
            abort(404)

        if request.method == 'GET':
            return (jsonify(obj.to_dict()))

        if request.method == 'DELETE':
            storage.delete(obj)
            storage.save()
            return (jsonify({}), 200)

        try:
            data = request.get_json()
        except:
            return (jsonify({"error": 'Not a JSON'}), 400)

        if request.method == 'PUT':
            for k, v in data.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(obj, k, v)
            storage.new(obj)
            storage.save()
            return (jsonify(obj.to_dict()), 200)

    else:
        if request.method == 'POST':
            try:
                data = request.get_json()
            except:
                return (jsonify({"error": 'Not a JSON'}), 400)
            if 'name' not in data.keys():
                return (jsonify({"error": 'Missing name'}), 400)
            obj = State(**data)
            storage.new(obj)
            storage.save()
            return (jsonify(obj.to_dict()), 201)

        else:
            return (jsonify([state.to_dict() for state in storage.all(
                    "State").values()]))

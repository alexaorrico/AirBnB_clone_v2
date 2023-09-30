#!/usr/bin/python3
""" states main file """

from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


def create(new_data, old_data=None):
    """ Create an existence object """
    try:
        values = {}
        new_state = State()

        if (old_data is None):
            if 'name' not in new_data:
                abort(400, description='Missing name')

            for key, value in new_data.items():
                setattr(new_state, key, value)

        else:

            for key, value in old_data.items():
                setattr(new_state, key, value)

            for key, value in new_data.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at':
                    setattr(new_state, key, value)

        for key, value in new_state.to_dict().items():
            values[key] = value

        new_state.save()

        return jsonify(values)

    except Exception:
        abort(400, description='Not a JSON')


def delete(state_id, update_flag=0):
    """ Delete an existence object """
    try:
        state = storage.get(State, state_id)

        if state is None:
            raise Exception

        storage.delete(state)
        storage.save()

        return make_response({}, 200)

    except Exception:
        abort(404)


def show(state_id=None):
    """ show an existence object/s """
    all_states = []
    values = {}
    if state_id is None:
        for string, state_item in storage.all('State').items():
            new_state = {}
            for key, value in state_item.to_dict().items():
                new_state[key] = value

            all_states.append(new_state)

        return jsonify(all_states)

    else:
        try:
            for key, value in storage.get(State, state_id).to_dict().items():
                values[key] = value

            return jsonify(values)
        except Exception:
            abort(404)


def update(state_id, new_data):
    """ Update an existence object """
    values = {}
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    try:
        for key, value in new_data.items():
            if (key != 'id' and key != 'created_at' and key != 'updated_at'):
                setattr(state, key, value)

        for key, value in state.to_dict().items():
            values[key] = value

        state.save()

        return jsonify(values)

    except Exception:
        abort(400, description='Missing name')


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Getting all the states or creating a new state """
    if request.method == 'GET':
        return show()
    else:
        new_data = request.get_json()
        return create(new_data)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state(state_id):
    """ A selected state """
    if request.method == 'GET':
        return show(state_id)

    elif request.method == 'DELETE':
        return delete(state_id, update_flag=0)

    else:
        new_data = request.get_json()
        return update(state_id, new_data)

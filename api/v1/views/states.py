#!/usr/bin/python3
""" API REST for State """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states')
def states_all():
    """ Route return all states """
    return jsonify(list(map(lambda x: x.to_dict(),
                            list(storage.all(State).values()))))


@app_views.route('/states/<id>')
def states_id(id):
    """ Route return states with referenced id """
    my_state = storage.get('State', id)
    try:
        return jsonify(my_state.to_dict())
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states_id(state_id):
    """ Route delete states with referenced id """
    my_object = storage.get('State', state_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_states():
    """ Route create states """
    if request.is_json:
        try:
            data = request.get_json()
            if 'name' in data:
                new_state = State(**data)
                new_state.save()
                return jsonify(new_state.to_dict()), 200
            else:
                return jsonify(error="Missing name"), 400
        except:
            return jsonify(error="Not a JSON"), 400
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_states(state_id):
    """ Route update states """

    if request.is_json:
        data = request.get_json()
        my_object = storage.get('State', state_id)
        if my_object is not None:
            for keys, values in data.items():
                if keys not in ["created_at", "updated_at", "id"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400

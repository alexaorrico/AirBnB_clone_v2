#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ list of state obj """
    st = storage.all("State")
    r = []
    for state in st.values():
        r.append(state.to_dict())
    return jsonify(r)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ fetches  object """
    st = storage.all("State")
    for key in st.keys():
        if key.split('.')[-1] == state_id:
            return jsonify(st.get(key).to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ del obj """
    st = storage.all("State")
    for key in st.keys():
        if key.split('.')[-1] == state_id:
            storage.delete(st.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creates """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('name' in dic.keys()):
        abort(400, "Missing name")
    st = State(**dic)
    st.save()
    return jsonify(st.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ updates obk """
    st = storage.all("State")
    state = None
    for key in st.keys():
        if key.split('.')[-1] == state_id:
            state = st.get(key)
    if not state:
        abort(404)
    nDict = request.get_json()
    if not nDict:
        abort(400, "Not a JSON")
    for key, value in nDict.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

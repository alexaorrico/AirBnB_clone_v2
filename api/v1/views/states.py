#!/usr/bin/python3
""" handles all default RESTFul API actions"""

from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route('/states', method=["GET"], strict_slashes=False)
def list_all():
    """lists all state objects with GET method"""
    stat = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(stat)


@app_views.route('/states/<id>', method=["GET"], strict_slashes=False)
def list_id(id):
    """lists state id with GET method"""
    retrieve_id = storage.get(State, id)
    if retrieve_id is None:
        abort(404)
    return jsonify(retrieve_id.to_dict())


@app_views.route('/states/<id>', method=["DELETE"], strict_slashes=False)
def delete_state(id):
    """deletes state id"""
    deleted = storage.get(State, id)
    if deleted is None:
        abort(404)
    storage.delete(deleted)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', method=["POST"], strict_slashes=False)
def post_state():
    """Posts a new state"""
    posts = request.get_json(silent=True)
    if posts is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in posts.keys() or posts["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    posts_obj = State(**posts)
    posts_obj.save()
    return make_response(jsonify(posts_obj.to_dict()), 201)


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def put_state_id(id):
    """Update State"""
    update = request.get_json(silent=True)
    if update is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    state = storage.get(State, id)
    if state is None:
        abort(404)
    lists = ["id", "created_at", "updated_at"]
    for key, value in update.items():
        if key in lists:
            continue
        setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()),200)
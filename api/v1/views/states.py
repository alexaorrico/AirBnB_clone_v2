#!/usr/bin/python3
"""blueprint for the states"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.get('/states', strict_slashes=False)
def get_states():
    """this is the view for the /api/v1/states
        endpoint"""
    all_states = [x.to_dict() for x in storage.all(State).values()]
    return jsonify(all_states)


@app_views.get('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """this is the view for the /api/v1/states/[SLUG]
        endpoint"""
    res = storage.get(State, escape(state_id))
    if not res:
        abort(404)
    res = res.to_dict()
    return jsonify(res)


@app_views.delete('/states/<state_id>', strict_slashes=False)
def delete_state(state_id):
    """this is the view for the /api/v1/states/[SLUG]
        endpoint"""
    res = storage.get(State, escape(state_id))
    if not res:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({})


@app_views.post('/states', strict_slashes=False)
def post_state():
    """this is the view for the /api/v1/states
        endpoint"""
    try:
        body = request.get_json()
        if 'name' not in body.keys():
            return make_response(jsonify("Missing name"), 400)
        new_state = State(**body)
        storage.new(new_state)
        storage.save()
        # all_states = [x.to_dict() for x in storage.all(State).values()]
        return make_response(jsonify(new_state.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.put('/states/<state_id>', strict_slashes=False)
def put_state(state_id):
    """this is the view for the /api/v1/states/[SLUG]
        endpoint"""
    res = storage.get(State, escape(state_id))
    if not res:
        abort(404)
    try:
        body = request.get_json()
        if 'name' not in body.keys():
            return make_response(jsonify("Missing name"), 400)
        for key in body:
            res.__dict__[key] = body[key]
        storage.save()
        # all_states = [x.to_dict() for x in storage.all(State).values()]
        return make_response(jsonify(res.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)

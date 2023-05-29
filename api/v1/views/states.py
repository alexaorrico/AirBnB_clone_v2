#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@authors: Robinson Montes
          Mauricio Olarte
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Create a new view for State objects that handles all default
    RestFul API actions.
    """
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in storage.all('State')
                        .values()])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif post.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        new_state = State(**post)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_state_id(state_id):
    """Retrieves a state object with a specific id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
                storage.save()
        return jsonify(state.to_dict()), 200

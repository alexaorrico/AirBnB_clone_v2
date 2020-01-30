#!/usr/bin/python3
"""
index route of the api
"""
from api.v1.views import app_views
from flask import jsonify, abort, requests
from models import storage
from json import loads

@app_views.route('/status')
def status():
    """ returns status for the api """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ retrieves the number of each objects by type """
    stats = {}
    stats['amenities'] = storage.count("Amenity")
    stats['cities'] = storage.count("City")
    stats['places'] = storage.count("Place")
    stats['reviews'] = storage.count("Review")
    stats['states'] = storage.count("State")
    stats['users'] = storage.count("User")
    return jsonify(stats)


@app_views.route('/states', methods=['GET'])
def states():
    """ Retrieves the list of all State objects """
    states = storage.all("State")
    result = []
    for state in states.values():
        result.append(state.to_dict())
    return jsonify(result)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieves a State object """
    states = storage.all("State")
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            return jsonify(states.get(key).to_dict())
    abort(404)
    return jsonify({"error": 404})


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    states = storage.all("State")
    for key in states.keys():
        if key.split('.')[-1] == state_id:
            storage.delete(states.get(key))
            return jsonify({}), 200
    abort(404)
    return jsonify({"error": 404})


@app_views.route('/states', methods=['POST'])
def post_state():
    """ Creates a State """
    body = request.get_json()
    try:
        dic = loads(body)
    except ValueError:
        abort(400, "Not a JSON")
    if not "name" in dic.keys():
        abort(400, "Missing name")
    state = State(dic)
    state.save()
    return jsonify(state.to_dict()), 201

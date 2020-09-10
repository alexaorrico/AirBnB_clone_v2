#!/usr/bin/python3
""" States handler of app """
from api.v1.views import app_views
from flask import jsonify, abort
from json import dumps
from models import storage



@app_views.route("/states", methods=["GET"])
def app_route():
    converted_states = []
    all_states = storage.all()
    for values in all_states.values():
        converted_states.append(values.to_dict())

    return jsonify(converted_states)


@app_views.route("/states/<states_id>", methods=["GET"])
def app_route2(states_id):
    search = storage.get("State", states_id)
    if search:
        return jsonify(search.to_dict())
    return abort(404)

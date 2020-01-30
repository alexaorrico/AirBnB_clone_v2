#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response, abort

@app_views.route('/states/',  methods=['GET'])
def states():
    """ Retrieve all the states"""

    data = storage.all('State')
    var = []

    for value in data.values():
        var.append(value.to_dict())

    return jsonify(var)

@app_views.route('/states/<state_id>',  methods=['GET'])
def states_id(state_id):
    """ Retrieve an state by id """
    data = storage.all('State')

    for key, value in data.items():
        key = key.split(".")

        if key[1] == state_id:
            return jsonify(value.to_dict())
    return make_response(jsonify({"Error", 404})

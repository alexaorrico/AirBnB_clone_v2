#!/usr/bin/python3
"""states"""

from models.state import State
from models.city import City
from flask import Flask, abort, jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    get_stat = storage.get(State, state_id)
    if not get_stat:
        abort(404)
    return jsonify(get_stat.cities)
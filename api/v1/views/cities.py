#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ tbc """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    states_cities = the_state.cities
    cities_list = []
    for item in states_cities:
        cities_list.append(item.to_dict())
    return jsonify(cities_list)


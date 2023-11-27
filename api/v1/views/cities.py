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


@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_all_cities(state_id):
    """ tbc """
    storage.reload()
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    cities_list = []
    cities_dict = storage.all(City)
    for item in cities_dict:
        if cities_dict[item].to_dict()['state_id'] == state_id:
            cities_list.append(cities_dict[item].to_dict())
    if cities_list is not None:
        return cities_list

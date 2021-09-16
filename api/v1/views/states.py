#!/usr/bin/python3
"""creates a new view for State Objects"""
from os import name
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """gets all state objects"""
    if request.method == 'GET':
        all_objects = storage.all(State)
        single_object = []
        for key, value in all_objects.items():
            single_object.append(value.to_dict)

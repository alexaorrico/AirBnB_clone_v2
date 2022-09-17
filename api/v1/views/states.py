#!/usr/bin/python3
from models.base_model import *
from flask import *
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id):
    """Retrieves state object"""
    if state_id is None:
        list_obj = []
        for i in storage.all('State'):
            list_obj = i.to_dict()
        return jsonify(list_obj)

    return storage.__dict__(list_obj)

#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''returns json to the route'''
    obj = [obj.to_dict() for obj in storage.all('State').values()]
    return jsonify(obj)

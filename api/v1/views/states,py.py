#!/usr/bin/python3

"""
State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():

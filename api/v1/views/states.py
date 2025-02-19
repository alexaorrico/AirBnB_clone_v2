#!/usr/bin/python3
""" State Module """
from api.v1.views import app_views
from flask import Flask
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_list():
    """ Method: Retrieve list of all State objects """


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_object():
    """ Method: Retrieve a State object """


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """ Method: Create a State """


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update():
    """ Method: Update State object """
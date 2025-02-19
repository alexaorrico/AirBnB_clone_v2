#!/usr/bin/python3
""" City Module """
from api.v1.views import app_views
from flask import Flask
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashses=False)
def city_list():
    """ Method: Retrieve list of all city objects of a state """


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_object():
    """ Method: Retrieve a city object """


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_delete():
    """ Method: Delete a city object """


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def city_create():
    """ Method: Create a city object """


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update():
    """ Method: Update a city object """
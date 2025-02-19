#!/usr/bin/python3
""" Place Module """
from api.v1.views import app_views
from flask import Flask
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place_list():
    """ Method: Retrieve list of all place objects of a City """


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_object():
    """ Method: Retrieve an place object """


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def place_delete():
    """ Method: Delete a place object """


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def place_create():
    """ Method: Create an place object """


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_update():
    """ Method: Update an place object """
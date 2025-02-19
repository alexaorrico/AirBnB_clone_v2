#!/usr/bin/python3
""" User Module """
from api.v1.views import app_views
from flask import Flask
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user_list():
    """ Method: Retrieve list of all amenity objects """


@app_views.route('/user/<user_id>', methods=['GET'], strict_slashes=False)
def user_object():
    """ Method: Retrieve an user object """


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    """ Method: Create an user object """


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_update():
    """ Method: Update an user object """
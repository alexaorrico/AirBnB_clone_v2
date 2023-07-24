#!/usr/bin/python3
""" Create a new view for states and handle RESTFul API """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City

@app_views.route('/cities', methods=['GET'], strict-slashes=False)
def get_cities():
    """ Retrieves teh lost of all City objects """
    cities = storage.all(City).values()
    return jsonify ([city.to dict() for city in cities])
#!/usr/bin/python3
""" Import the app_views blueprint for cities API endpoints """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def get_all_cities(state_id):
    """ Get all cities objects """
    all_status = storage.all("State").values()
    state_objs = [state.to_dict() for state in all_status if state_id == state.id]
    if state_objs == []:
        abort(404)
    all_cities = storage.all("City").values()
    list_cities = [city.to_dict() for city in all_cities if state_id == city.state_id]
    return jsonify(list_cities)

#!/usr/bin/python3
'''
API module to create cities
'''
from models import storage
from models.state import State
from models.city import City
from flask import request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    '''
    finds all city objects and returns them
    '''
    all_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    """ else:
        for i in storage.all("State").values():
            all_cities.append(i.to_dict()) """

    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state_id:
            print(city.state_id)
            all_cities.append(city.to_dict())
            print(all_cities)
    return jsonify(all_cities)


#@app_views.route

#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify

@app_views.route('/states')
def show_states():
    """ show states"""
    new_list = []
    my_dict = storage.all(State)

    for key, value in my_dict.items():
        new_list.append(value.to_dict())
    return jsonify(new_list)

@app_views.route('/states/')
@app_views.route('/states/<state_id>')
def show_states_id(state_id):
    """ show ID'state"""
    my_dict = storage.get(State ,state_id)
    if my_dict is not None:
        return my_dict
    else:
        raise 404
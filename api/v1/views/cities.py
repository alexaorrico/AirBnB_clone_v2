#!/usr/bin/python3
"""
Handle all default RESTFUL API actions
"""
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=('GET'))
def cities_in_state(state_id):
    """ Returns all cities in a state id"""
    all_states = State.to_dict()
    for key, val in all_states.items():
	if val['state_id'] == state_id:
            st_id = all_states[key]
            break
        else:
            st_id = None
    

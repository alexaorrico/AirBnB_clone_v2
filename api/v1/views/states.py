"""Module to create a new view for State objects"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states = storage.all('State')
    my_list = []
    for value in all_states.values():
        my_list.append(value.to_dict())
    return jsonify(my_list)

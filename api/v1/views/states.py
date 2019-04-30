from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State
"""Routing for AirBnB state object"""


@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    if request.method == 'GET':
        dic = storage.all(State)
        if state_id is None:
            states_list = []
            for key, value in dic.items():
                states_list.append(value.to_dict())
            return jsonify(states_list)
        else:
            for key, value in dic.items():
                if value.id == state_id:
                    return jsonify(value.to_dict())
            return abort(404)

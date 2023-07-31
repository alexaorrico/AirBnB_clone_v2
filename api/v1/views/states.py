"""State view for the web service API"""
from flask import jsonify, abort, request
from api.v1.views import app_views  # Blueprint object
from models import storage
from models.state import State


# Route to get States
@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """Return a JSON reponse of all state objects,
        or object of a specified id
    """

    if state_id:
        # Get dictionary of state object by id
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    else:
        # Get list of state objects dictionary
        state_objs = [v.to_dict() for k, v in storage.all(State).items()]
        return jsonify(state_objs)


# Route to delete a state object


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Delete a state object specified by it id"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
    return jsonify({}), 200

# Route to create a state object


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Create a new state object"""

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    if 'name' not in content:
        abort(400, 'Missing name')  # raise bad request error
    state = State(**content)
    state.save()

    return jsonify(state.to_dict()), 201

# Route to update a state object


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Update a state object specified by id"""

    state = storage.get(State, state_id)  # Get state by id

    if not state:
        abort(404)  # raise not found error

    content = request.get_json()  # Content body
    if type(content) is not dict:
        abort(400, 'Not a Json')  # raise bad request error
    for key, value in content.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)  # Update state with new data
            state.save()

    return jsonify(state.to_dict()), 200

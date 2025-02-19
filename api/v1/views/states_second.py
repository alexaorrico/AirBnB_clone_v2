#!/usr/bin/python3
"""State"""
from flask import jsonify, abort, request
from models.state import State  # Import the State model
from models import storage  # Import the storage object
from api.v1.views import app_views


# Define the route for handling GET and POST requests for all states
# and DELETE, GET, PUT requests for specific state by ID
@app_views.route("/states", methods=["GET", "POST"],
                 strict_slashes=False)
@app_views.route("/states/<state_id>",
                 methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def stateEdit(state_id=None):
    """
    Edit the State objects according to the specified HTTP method:
      - GET: Retrieves the list of all State objects.
             Or one object if ID is passed.
      - DELETE: Deletes object what have the passed ID.
                Or returns 404 page if no ID passed.
      - POST: Add a new state object if name provided.
              Returns error code if not.
      - PUT: Update object if name provided.
             Returns error code if not.
    """
    # Get all states objects
    fullList = storage.all(State)

    # Using HTTP GET
    if request.method == "GET":
        if not state_id:
            # Retrieve all states
            data = [state.to_dict() for state in fullList.values()]
            return jsonify(data)
        else:
            # Retrieve specific state by ID
            seek = "State." + state_id
            try:
                data = fullList[seek].to_dict()
                return jsonify(data)
            except KeyError:
                abort(404)

    # Using HTTP DELETE
    elif request.method == "DELETE":
        try:
            seek = "State." + state_id
            state_to_delete = fullList.get(seek)
            if state_to_delete:
                storage.delete(state_to_delete)
                storage.save()
                return jsonify({}), 200
            else:
                abort(404)
        except Exception:
            abort(404)

    # Using HTTP POST
    elif request.method == "POST":
        if request.is_json:
            new_state_data = request.get_json()
        else:
            abort(400, "Not a JSON")
        if "name" in new_state_data:
            new_state = State(**new_state_data)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
        else:
            abort(400, "Missing name")

    # Using HTTP PUT
    elif request.method == "PUT":
        seek = "State." + state_id
        try:
            found_state = fullList[seek]
            if request.is_json:
                data_to_update = request.get_json()
            else:
                abort(400, "Not a JSON")
            for key, value in data_to_update.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(found_state, key, value)
            storage.save()
            return jsonify(found_state.to_dict()), 200
        except KeyError:
            abort(404)

    else:
        abort(501)

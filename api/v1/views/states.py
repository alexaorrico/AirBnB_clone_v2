# #!/usr/bin/python3
# """
# states.py
# """
# from . import app_views
# from flask import jsonify
# from models import storage
# from models.state import State
# from flask import abort, request, Response, make_response
# import json


# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def allstates():
#     """
#     Retrieves the list of all State objects
#     """
#     dict_of_states = [obj.to_dict() for obj in storage.all(State).values()]
#     response = Response(
#         response=json.dumps(dict_of_states, indent=4),
#         status=200,
#         mimetype='application/json'
#     )
#     return response


# @app_views.route('/states/<state_id>',
#                  methods=['GET'], strict_slashes=False)
# def state_by_id(state_id):
#     """
#     Retrieves a State object:
#     GET /api/v1/states/<state_id>
#     """
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     return jsonify(state.to_dict())


# @app_views.route('/states/<state_id>',
#                  methods=['DELETE'], strict_slashes=False)
# def delete_by_id(state_id):
#     """
#     Deletes a State object::
#     DELETE /api/v1/states/<state_id>
#     """
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     storage.delete(state)
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def create_state():
#     """
#     Creates a new State object
#     """
#     data = request.get_json()
#     if not data:
#         abort(400, 'Not a JSON')
#     if 'name' not in data:
#         abort(400, 'Missing name')

#     new_state = State(**data)
#     new_state.save()

#     return jsonify(new_state.to_dict()), 201

# @app_views.route('/states/<state_id>',
#                  methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """
#     updates a new State object
#     """
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     data = request.get_json()
#     if not data:
#         abort(400, 'Not a JSON')
#     ignored_keys = ['id', 'updated_at', 'created_at']
#     for key, value in data.items():
#         if key in ignored_keys:
#             continue
#         setattr(state, key, value)
#     state.save()
#     return jsonify(state.to_dict()), 200

#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get():
    result = []
    """ get all the objects from state """
    for i in storage.all("State").values():
        result.append(i.to_dict())
    return jsonify(result)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_specific(state_id):
    """ get the specific object from state """
    for i in storage.all("State").values():
        if i.id == state_id:
            return i.to_dict()
    abort(404)


@app_views.route("/states/<state_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def state_specific_delete(state_id):
    """ delete the inputed object from state """
    task = [task for task in storage.all(
        "State").values() if task.id == state_id]
    if len(task) == 0:
        abort(404)
    storage.delete(task[0])
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def state_specific_post():
    """ post the inputed object from state """
    if not request.json:
        return make_response("Not a JSON", 400)
    if 'name' not in request.json:
        return make_response("Missing name", 400)
    obj = classes["State"]
    new_inst = obj(**request.json)
    new_inst.save()
    return new_inst.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_specific_put(state_id):
    """ update the specific object from state """
    instance = None
    if not request.json:
        return make_response("Not a JSON", 400)
    check = ["id", "created_at", "updated_at"]
    for i in storage.all("State").values():
        if i.id == state_id:
            instance = i
            for key, value in request.json.items():
                if key not in check:
                    setattr(i, key, value)
                    i.save()
    if not instance:
        abort(404)
    return instance.to_dict(), 200

#!/usr/bin/python3
"""modify state objects via APIs"""
from models.state import State
from flask import jsonify, make_response, abort, request
from models import storage
from api.v1.views import app_views


def abortNotExists(cls, obj_id):
    """exit with a 404 status if obj not found"""
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_states(state_id=None):
    """retrieve a state object"""
    if not state_id:
        objs_dict = storage.all(State)
        obj_list = []
        for obj in objs_dict.values():
            obj_list.append(obj.to_dict())
        return make_response(jsonify(obj_list))

    else:
        obj = abortNotExists(State, state_id)
        return make_response(jsonify(obj.to_dict()))


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_states():
    """create a new state object"""
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")

    new_obj = State(**data)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    obj = abortNotExists(State, state_id)
    storage.delete(obj)
    storage.save()
    return make_response({}, 200)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    obj = abortNotExists(State, state_id)
    try:
        data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)

    storage.save()
    return make_response(obj.to_dict(), 200)

#     def put(self, state_id):
#         """Updates a State object: PUT /api/v1/states/<state_id>"""
#         obj = abortNotExists(State, state_id)
#         try:
#             data = request.get_json()
#         except Exception:
#             abort(400, description="Not a JSON")

#         for key, val in data.items():
#             if key not in ["id", "created_at", "updated_at"]:
#                 setattr(obj, key, val)

#         storage.new(obj)
#         return obj.to_dict(), 200

# class State_view_all(Resource):
#     """handle all states requests without id"""
#     def get(self):
#         """get all state objects"""
#         objs_dict = storage.all()
#         obj_list = []
#         for obj in objs_dict.values():
#             obj_list.append(obj.to_dict())
#         return jsonify(obj_list)

#     def post(self):
#         """Creates a State: POST /api/v1/states"""
#         try:
#             data = request.get_json()
#         except Exception:
#             abort(400, description="Not a JSON")
#         if "name" not in data.keys():
#             abort(400, description="Missing name")

#         new_obj = State(**data)
#         storage.new(new_obj)
#         return new_obj.to_dict(), 201


# class State_view(Resource):
#     """handle all states requests with id"""
#     def get(self, state_id):
#         """Retrieves a State object: GET /api/v1/states/<state_id>"""
#         obj = abortNotExists(State, state_id)
#         return jsonify(obj.to_dict())

#     def delete(self, state_id):
#         """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
#         obj = abortNotExists(State, state_id)
#         storage.delete(obj)
#         return {}, 200

#     def put(self, state_id):
#         """Updates a State object: PUT /api/v1/states/<state_id>"""
#         obj = abortNotExists(State, state_id)
#         try:
#             data = request.get_json()
#         except Exception:
#             abort(400, description="Not a JSON")

#         for key, val in data.items():
#             if key not in ["id", "created_at", "updated_at"]:
#                 setattr(obj, key, val)

#         storage.new(obj)
#         return obj.to_dict(), 200

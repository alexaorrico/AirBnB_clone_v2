#!/usr/bin/python3
'''Module containing instructions for the flask blueprint app_views'''
from api.v1.views import app_views
from api import mapped_classes
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    '''Retrieves all state objects and returns them in JSON form'''
    content = storage.all("State")
    rqd_info = []
    for key, value in content.items():
        rqd_info.append(value.to_dict())
    return jsonify(rqd_info)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def new_state():
    '''Creates a State object with the values in the request'''
    post_dict = request.get_json()
    if not post_dict:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in post_dict:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = mapped_classes["State"](**post_dict)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    '''Return the JSON format of a specific request id,
    otherwise, raise a 404
    '''
    cls_obj = storage.get("State", state_id)
    if cls_obj is None:
        abort(404)
    else:
        return jsonify(cls_obj.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_spcific_state(state_id):
    '''Deletes a state by given id else raise a 404'''
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_specific_state(state_id):
    '''Updates state information specific to the given id,
    else raise a 404 error
    '''
    cls_obj = storage.get("State", state_id)
    if cls_obj is None:
        abort(404)
    else:
        update_dict = request.get_json()
        if not update_dict:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        update_dict.pop("id", None)
        update_dict.pop("created_at", None)
        update_dict.pop("updated_at", None)
        for key, value in update_dict.items():
            setattr(cls_obj, key, value)
        cls_obj.save()
        return jsonify(cls_obj.to_dict()), 200

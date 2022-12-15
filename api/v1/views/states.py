from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.state import State

@app_views.route('/states', methods =['GET'], defaults={'state_id':None})
@app_views.route('/states/<state_id>', methods=['GET'])
def getState(state_id):
    """just hoping this is a mistake"""
    list_objects = []
    if state_id and storage.get(State, "state_id") is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    for i in storage.get(State, state_id):
        list_objects.append(i)
        return jsonify(list_objects)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def statusDeletes(state_id):
    """statusDeletes delete a state"""
    if storage.get(State, state_id):
            storage.delete(storage.get(State, state_id))
            storage.save()
            return make_response(jsonify({}, 200))
    else:
        return make_response(jsonify({"error": "Not found"}), 404)
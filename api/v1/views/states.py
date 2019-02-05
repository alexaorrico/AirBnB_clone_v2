#!/usr/bin/python3
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def showStates():
    """ Shows all states in the file storage """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states/<id>', strict_slashes=False, methods=['GET'])
def a_states_id(id):
    """ Gets the state and its id if any """
    for s_id in storage.all('State').values():
        if s_id.id == id:
            return jsonify(s_id.to_dict())
        else:
            return (jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<id>', strict_slashes=False, methods=["DELETE"])
def del_states_id(id):
    """ deletes a sate if given the id """
    for s_id in storage.all('State').values():
        if s_id.id == id:
            return jsonify(s_id.delete())
        else:
            return (jsonify({"error": "Not found"}), 404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def postStates():
    """ creates a new state """
    thing = request.get_json()
    if thing is None or len(thing) == 0:
        return (jsonify({"error": "Not a JSON"}), 400)
    state = thing.get("name")
    if state is None or len(thing) == 0:
        return (jsonify({"error": "Missing name"}), 400)
    s = State()
    s.name = state
    s.save()
    return (jsonify(s.to_dict()), 201)


if __name__ == '__main__':
    if not environ.get('HBNB_API_HOST'):
        environ['HBNB_API_HOST'] = '0.0.0.0'
    if not environ.get('HBNB_API_PORT'):
        environ['HBNB_API_HOST'] = '5000'
    app.run(host=environ['HBNB_API_HOST'],
            port=environ['HBNB_API_PORT'],
            threaded=True)

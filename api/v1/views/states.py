from models.user import User
from models.db_storage import DBStorage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from



@app_views.route('/states', methods=['GET', 'POST'])
@swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def states_no_id():
    """states route to handle states"""
    if request.method == 'GET':
        all_states = storage.all(State)
        all_states = list(obj.to_json() for obj in all_states.values())
        return jsonify(all_states)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = storage.classes.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 200



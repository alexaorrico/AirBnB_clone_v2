#!/usr/bin/python3
""" API redirections """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from werkzeug.exceptions import BadRequest

# Status
@app_views.route('/states/status')
def states_status():
    """ returns status OK if app is working """
    return jsonify({"Status": "OK"})

# All
@app_views.route('/states', strict_slashes=False)
def states_all():
    """ retrieves a list of all states objects """
    ret_list = []
    for obj in storage.all(State).values():
        ret_list.append(obj.to_dict())
    return jsonify(ret_list)

# Get by id
@app_views.route('/states/<state_id>', 
                 methods = ['GET'], 
                 strict_slashes=False)
def states_get(state_id):
    """ retrieves a specific state object based on id """
    obj = storage.get(State, state_id)
    if (obj): return jsonify(obj.to_dict())
    else: abort(404)

# Delete by id
@app_views.route('/states/<state_id>', 
                 methods = ['DELETE'], 
                 strict_slashes=False)
def states_del(state_id):
    """ delete linked state object  """
    obj = storage.get(State, state_id)
    if obj not None:
        storage.delete(obj)
    else: abort(404)

# Create new
@app_views.route('/states/<state_id>',
                 methods = ['POST'],
                 strict_slashes=False)
def states_new(state_id):
    try: 
        data = request.get_json()
    except BadRequest: 
        abort(400, description="Not a JSON")
    if not data.get('name'):
        abort(400, description="Missing name")

    storage.new(data)
    return storage.get(State, state_id)



#!/usr/bin/python3
"""
    HBNB_V3: Task 7
"""
from api.v1.views.index import app_views
from api.v1.views import State
from models import storage
from flask import jsonify, request, abort

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def viewallthestatethings():
    """Retrieves the list of all State objects"""
    from models import storage
    from models.state import State

    if request.method == 'GET':
        stl = storage.all(State)
        li = []
        for state in stl.values():
            li.append(state.to_dict())
        return jsonify(li)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if "name" not in body.keys():
                abort(400, "Missing name")
            else:
                newstate = State()
                newstate.__dict__.update(body)
                newstate.save()
                return jsonify(newstate.to_dict()), 201
                

        except ValueError:
            abort(400, "Not a JSON")



@app_views.route('/states/<state_id>', strict_slashes=False,
        methods=['GET', 'DELETE', 'PUT'])
def stateidtime(state_id):
    """Handles a state object with said id depending on HTTP request"""
    stl = storage.all(State)
    k = "State." + state_id
    if k in stl.keys():
        s = stl.get(k)
        sd = s.to_dict()
        if request.method == 'GET':
            return jsonify(sd)
        if request.method == 'DELETE':
            storage.delete(s)
            storage.save()
            return jsonify({})
        if request.method == 'PUT':
            try:
                body = request.get_json()
                body.pop("id", "")
                body.pop("created_at", "")
                body.pop("updated_at", "")
                s.__dict__.update(body)
                s.save()
                sd = s.to_dict()
                return jsonify(sd)

            except ValueError:
                abort(400, "Not a JSON")

            
    else:
        abort(404)

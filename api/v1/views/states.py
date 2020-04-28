#!/usr/bin/python3

from models.base_model import *
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
    

@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    ls = []
    objects = storage.all()
    if request.method == "GET":
        for key, value in objects.items():
            ls.append(value.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif not 'name' in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
           new = State(request.json)
           new.save()
           


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    objects = storage.all()
    for key, value in objects.items():
        if state_id == value.id:
            if request.method == "GET":
                return value.to_dict()
            elif request.method == "DELETE":
                storage.delete(value)
                storage.save()
                return {}
    abort(404)

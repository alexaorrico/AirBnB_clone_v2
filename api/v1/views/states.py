#!/usr/bin/python3

from api.v1.views import app_views
from models import storage
import flask
from flask import request, jsonify, abort
from models.state import State
from models.base_model import BaseModel


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def http_action():
    if request.method == "GET":
        dic = []
        for value in storage.all(State).values():
            dic.append(BaseModel.to_dict(value))
        return flask.jsonify(dic)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'], strict_slashes=False) 
def http_actions(state_id):
    dic = storage.get(State, state_id) 
    if request.method == "GET":
        if dic is not None:
            return flask.jsonify(BaseModel.to_dict(dic))
        else:
            raise abort(404)
    elif request.method == "DELETE":
        return "A POST has been received!"
        

            

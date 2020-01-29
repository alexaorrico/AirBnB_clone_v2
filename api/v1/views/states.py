#!/usr/bin/python3
""" states api"""

from flask import jsonify
from models import storage
from models.state import State
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
def state_obj(state_id=None):
    """ states api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if state_id is None:
            mylist = apimethod.get_objects(State)
            return make_response(jsonify(mylist), 200)

        else:
            mydict = apimethod.get_one_object("State", state_id)
            if not mydict:
                abort(404)
            else:
                return make_response(jsonify(mydict))

    if request.method == 'DELETE':
        if state_id:
            deleteObj = apimethod.delete_one_object("State", state_id)
            if not deleteObj:
                abort(404)
            else:
                return make_response(jsonify({}, 200))
        else:
            abort(400)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")

        mydict = request.get_json()

        newObjDict = apimethod.create_object(State, **mydict)
        return make_response(jsonify(newObjDict), 201)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)

        updObjDict = apimethod.update_objects("State", state_id, **mydict)
        if updObjDict:

            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)

#!/usr/bin/python3
""" cities api"""

from flask import jsonify
from models import storage
from models.city import City
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/states/<state_id>/cities",
                 methods=['GET', 'POST'], strict_slashes=False)
def city_state(state_id=None):
    """ cities api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if not state_id:
            abort(400)
        mylist = apimethod.get_object_byid("State", state_id)
        if mylist:
            return make_response(jsonify(mylist), 200)
        else:
            abort(404)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")

        mydict = request.get_json()
        myobj = storage.get('State', state_id)
        if myobj:
            mydict['state_id'] = state_id
            newObjDict = apimethod.create_object(City, **mydict)
        else:
            abort(404)
        return make_response(jsonify(newObjDict), 201)


@app_views.route("/cities/<city_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city(city_id=None):
    """ cities api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if not city_id:
            abort(400)
        mydict = apimethod.get_one_object("City", city_id)
        if not mydict:
            abort(404)
        else:
            return make_response(jsonify(mydict), 200)
    if request.method == 'DELETE':
        if city_id:
            deleteObj = apimethod.delete_one_object("City", city_id)
            if not deleteObj:
                abort(404)
            else:
                return make_response(jsonify({}, 200))
        else:
            abort(400)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at', 'state_id']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)
        updObjDict = apimethod.update_objects("City", city_id, **mydict)
        if updObjDict:

            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)

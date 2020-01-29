#!/usr/bin/python3
""" user api"""

from flask import jsonify
from models import storage
from models.user import User
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'])
def user_obj(user_id=None):
    """ user api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if user_id is None:
            mylist = apimethod.get_objects(User)
            return make_response(jsonify(mylist), 200)

        else:
            mydict = apimethod.get_one_object("User", user_id)
            if not mydict:
                abort(404)
            else:
                return make_response(jsonify(mydict))

    if request.method == 'DELETE':
        if user_id:
            deleteObj = apimethod.delete_one_object("User", user_id)
            if not deleteObj:
                abort(404)
            else:
                return make_response(jsonify({}, 200))
        else:
            abort(400)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'email' not in request.json:
            abort(400, "Missing email")
        if 'password' not in request.json:
            abort(400, "Missing password")

        mydict = request.get_json()

        newObjDict = apimethod.create_object(User, **mydict)
        return make_response(jsonify(newObjDict), 201)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at', 'email']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)

        updObjDict = apimethod.update_objects("User", user_id, **mydict)
        if updObjDict:

            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)

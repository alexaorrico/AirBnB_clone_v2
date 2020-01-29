#!/usr/bin/python3
""" Review api"""

from flask import jsonify
from models import storage
from models.review import Review
from api.v1.views import app_views
from api.v1.views import *
from api.v1.views.methods import ApiMethod
from flask import abort, request, make_response


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET', 'POST'], strict_slashes=False)
def review_place(place_id=None):
    """ place api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if not place_id:
            abort(400)
        mylist = apimethod.get_object_byid("Place", place_id)
        if mylist:
            return make_response(jsonify(mylist), 200)
        else:
            abort(404)

    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'user_id' not in request.json:
            abort(400, "Missing user_id")
        if 'text' not in request.json:
            abort(400, "Missing text")

        mydict = request.get_json()
        myuser = storage.get('User', mydict['user_id'])
        if not myuser:
            abort(404)
        myobj = storage.get('Place', place_id)
        if myobj:
            mydict['state_id'] = state_id
            newObjDict = apimethod.create_object(City, **mydict)
        else:
            abort(404)
        return make_response(jsonify(newObjDict), 201)


@app_views.route("/reviews/<review_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review(review_id=None):
    """ review api"""
    apimethod = ApiMethod()
    if request.method == 'GET':
        if not review_id:
            abort(400)
        mydict = apimethod.get_one_object("Review", review_id)
        if not mydict:
            abort(404)
        else:
            return make_response(jsonify(mydict), 200)
    if request.method == 'DELETE':
        if review_id:
            deleteObj = apimethod.delete_one_object("Review", review_id)
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

        list = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)
        updObjDict = apimethod.update_objects("Review", review_id, **mydict)
        if updObjDict:

            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)

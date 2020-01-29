#1/usr/bin/python
"""amenities routes api"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import *
from api.v1.views.methods import ApiMethod


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'])
def amenity_obj(amenity_id=None):
    """amenity api method"""
    am = ApiMethod()
    if request.method == 'GET':
        if amenity_id is None:
            mylist = am.get_objects(Amenity)
            return make_response(jsonify(mylist), 200)

        else:
            mydict = am.get_one_object("Amenity", amenity_id)
            if not mydict:
                abort(404)
            else:
                return make_response(jsonify(mydict))

    if request.method == 'DELETE':
        if amenity_id:
            deleteObj = am.delete_one_object("Amenity", amenity_id)
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

        newObjDict = am.create_object(Amenity, **mydict)
        return make_response(jsonify(newObjDict), 201)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        mydict = request.get_json()

        list = ['id', 'created_at', 'updated_at']
        for key in list:
            if key in mydict.keys():
                mydict.pop(key)

        updObjDict = am.update_objects("Amenity", amenity_id, **mydict)
        if updObjDict:
            return make_response(jsonify(updObjDict), 200)
        else:
            abort(404)

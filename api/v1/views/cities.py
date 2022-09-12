#!/usr/bin/python3
"""Same as State, create a new view for City\
objects that handles all default RESTFul API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import City
from werkzeug.exceptions import BadRequest


# Status
@app_views.route('/cities/status')
def cities_status():
    """ returns status OK if app is working """
    return jsonify({"Status": "OK"})


# All
@app_views.route('/cities', strict_slashes=False)
def cities_all():
    """ retrieves a list of all states objects """
    ret_list = []
    for obj in storage.all(City).values():
        ret_list.append(obj.to_dict())
    return jsonify(ret_list)


# Get by id
@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def cities_get(city_id):
    """ retrieves a specific state object based on id """
    obj = storage.get(City, city_id)
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


# Delete by id
@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def cities_del(city_id):
    """ delete linked state object """
    obj = storage.get(City, city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return {}
    else:
        abort(404)


# Create new
@app_views.route('/cities/',
                 methods=['POST'],
                 strict_slashes=False)
def cities_new():
    try:
        obj_JSON = request.get_json()
        new_obj = City(**obj_JSON)
        if not obj_JSON.get('name'):
            abort(400, description="Missing name")
    except BadRequest:
        abort(400, description="Not a JSON")

    storage.new(new_obj)
    storage.save()
    return jsonify(storage.get(new_obj.__class__, new_obj.id).to_dict())


# Update
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_put(city_id):
    """ Handles PUT request. Updates a State obj with status 200, else 400 """
    ignore_keys = ['id', 'created_at', 'updated_at']
    obj = storage.get(City, city_id)
    attrs = request.get_json(force=True, silent=True)
    if not obj:
        abort(404)
    if attrs is None:
        abort(400, "Not a JSON")
    else:
        for key, value in attrs.items():
            if key in ignore_keys:
                continue
            setattr(obj, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200

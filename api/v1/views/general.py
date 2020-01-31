from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
"""
    general stuff
"""


def get_obj(obj):
    """ get """
    if obj:
        return (jsonify(obj.to_dict()), 200)
    return abort(404)


def put_obj(obj):
    """ put """
    if not state:
        abort(404)
    try:
        data = request.get_json()
    except:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, data[key])
    storage.save()
    return (jsonify(state.to_dict()), 200)


def delete_obj(obj):
    """ delete """
    if not state:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify(dict()), 200)


methods = {
    "GET": get_obj,
    "PUT": put_obj,
    "DELETE": delete_obj,
}


def do(cls, id=None):
    """ general """
    if id:
        for obj in storage.all(cls).values():
            if obj.id == id and request.method in methods:
                return methods[request.method](obj)
    elif request.method == "GET":
        return (jsonify([
            s.to_dict() for s
            in storage.all(cls).values()
        ]), 200)
    elif request.method == "POST":
        try:
            data = request.get_json()
        except:
            abort(400, "Not a JSON")
        if not data or "name" not in data:
            abort(400, "Missing name")
        new = cls()
        for key in data:
            setattr(new, key, data[key])
        new.save()
        return (jsonify(new.to_dict()), 201)
    return {"error": "Not found"}, 404

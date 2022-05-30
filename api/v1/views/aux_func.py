#!/usr/bin/python3
"""
----------------
Call the methods
----------------
"""
from models.state import City
from models import storage
from flask import jsonify, abort


def aux_func(cls, met, id=None):
    """
    ----------------------
    Return the jsonify obj
    ----------------------
    """
    objs = storage.all(cls)
    if met == "GET":
        if id:
            obj = storage.get(cls, id)
            if obj:
                return jsonify(obj.to_dict())
            else:
                abort(404)
        else:
            result = []
            for obj in objs.values():
                result.append(obj.to_dict())
            return jsonify(result)
    elif met == "DELETE":
        if id:
            key = "{}.{}".format(cls.__name__, id)
            if key in objs.keys():
                objs[key].delete()
                # No sabemos si hay que guardar
                storage.save()
                return jsonify({}), 200, {'Content-Type': 'application/json'}
        abort(404)

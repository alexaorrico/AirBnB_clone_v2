#!/usr/bin/ python3
"""
Creates a status route
"""


from flask import jsonify
from api.v1 import views

from models.engine.db_storage import DBStorage
import models

my_app = views.app_views


@my_app.route('/status')
def getStatus():
    """returns the status of the API."""

    return jsonify({"status": "OK"})

@my_app.route('/stats')
def numObj():
    """returns the number of each object by type."""
    objCount = DBStorage.count
    my_objs = DBStorage.all()

    for key, value in my_objs.items():
        obj_name = key.split('.')[0]
        obj_id = key.split('.')[1]
        return objCount(obj_name, obj_id)

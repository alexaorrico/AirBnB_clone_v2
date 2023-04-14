#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify

from models import storage
from models import class_models


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """
    classes = sorted(
        class_models,
        key=(lambda x: x.__name__[0])
    )
    num_objs = {
        x.get_plural(): storage.count(x) for x in classes
    }
    return jsonify(num_objs)

#!/usr/bin/python3
""" v1 view main file """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes_plural


@app_views.route('/status')
def get_status():
    """ return the status """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """ return the stats """
    classes_count = {}
    for class_name in classes_plural:
        classes_count[class_name] = storage.count(classes_plural[class_name])

    return jsonify(classes_count)

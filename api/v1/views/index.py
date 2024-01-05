#!/usr/bin/python3
"""
set up route for status endpoint
"""


from api.v1.views import app_views
from flask import jsonify
from models.engine.db_storage import classes
import models


@app_views.route('/status')
def get_status():
    """ send status api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_count():
    classes_counts = dict(
        (cls.__name__, models.storage.count(cls)) for cls in classes.values()
    )
    return jsonify(classes_counts)

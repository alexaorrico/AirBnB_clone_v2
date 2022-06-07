#!/usr/bin/python3
"""index"""

from flask import jsonify
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views

@app_views.route("/status", methods=["GET"])
def status_view():

    return jsonify(
        {
            "status": "OK"
        }
        )

@app_views.route("/stats")
def stats_view():
    stat_dict = {}
    for k, v in classes.items():
        stat_dict[k] = storage.count(v)

    return jsonify(stat_dict)
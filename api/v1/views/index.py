#!/usr/bin/python3
"""Defines a function"""
from flask.json import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Defines a status route returning a json object of the api status.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns all stored entities from storage"""
    from models import storage, model_mapping
    entity_count_map = {}
    for entity in model_mapping:
        entity_count = storage.count(entity)
        entity_count_map[model_mapping[entity]] = entity_count
    return (jsonify(entity_count_map))

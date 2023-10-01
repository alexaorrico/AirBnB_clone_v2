#!/usr/bin/python3
"""
The index module
"""

from flask import Blueprint, jsonify
from api.v1.views import app_views
from models.engine import db_storage


api_v1_stats = Blueprint('api_v1_stats', __name__)


@app_views.route('/status')
def status():
    """ Returns status of the api """
    return jsonify({"status": "OK"})


@api_v1_stats.route('/api/v1/stats', methods=['GET'])
def get_object_count():
    """ Returns object count """
    storage = db_storage.DBStorage()

    counts = storage.count()

    return jsonify(counts)

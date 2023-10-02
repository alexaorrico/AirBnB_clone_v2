#!/usr/bin/python3
"""
The index module
"""

from flask import Flask, Blueprint, jsonify
from models import storage

app = Flask(__name__)
api_v1_stats = Blueprint("api_v1_stats", __name__)


@app.route("/status", methods=["GET"])
def status():
    """Returns status of the api"""
    return jsonify({"status": "OK"})


#@app_v1_stats.route("/stats", methods=["GET"])
@app.route('/stats', methods=["GET"])
def get_object_count():
    """Returns object count"""
    storage = db_storage.DBStorage()

    counts = storage.count()

    return jsonify(counts)

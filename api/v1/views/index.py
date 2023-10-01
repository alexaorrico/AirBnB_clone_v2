#!/usr/bin/python
"""
The index module
"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models.engine import db_storage


api_v1_stats = Blueprint('api_v1_stats', __name__)
app = Flask(__name__)


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@api_v1_stats.route('/api/v1/stats', methods=['GET'])
def get_object_count():
    storage = db_storage.DBStorage()

    counts = storage.count()

    return jsonify(counts)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/python3
""" index"""

from flask import Flask, jsonify, Blueprint
from api.v1.views import app_views

app = Flask(__name__)
status_bp = Blueprint('status', __name__)

@status_bp.route('/status', methods=['GET'])
def status():
    return jsonify ({'status': 'OK'})

app.register_blueprint(status_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

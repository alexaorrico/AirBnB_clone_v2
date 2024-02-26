#!/usr/bin/python3
""" index"""

from flask import jsonify, Blueprint

app_views = Blueprint('app_views', __name__)


@app_views.route('/api/v1/status', methods=['GET'])
def get_status():
    """Retrieve the status"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from flask import Blueprint, jsonify
""" route that returns a JSON with status ok"""

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON with status: OK"""
    return jsonify({"status": "OK"})


from . import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """returns status ok"""
    return jsonify(f'{\n\t"status": "ok"\n}')

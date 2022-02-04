#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from api.v1.views import app_views
# Si descomentamos la linea 6, aparece una asignación circular.
from flask import jsonify

#app_views = Flask(__name__)


@app_views.route('/status')
def status():
    """ Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})

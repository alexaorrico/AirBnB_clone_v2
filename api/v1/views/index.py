#!/usr/bin/python3
"""Doc"""
from views import app_views
from flask import jsonify, Flask

app = Flask(__name__)

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def index():
    """ returns a JSON """
    return jsonify(status="OK")

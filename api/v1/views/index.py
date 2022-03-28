#!/usr/bin/py
"""
This module shows roots for our site
"""
from Flask import Flask, jsonify
from api.v1.views import app_views
app = Flask(__name__)


@app_views.route('/status')
def status():
    """Returns status of the website if running"""
    status = {'status': 'OK'}
    return jsonify(status)

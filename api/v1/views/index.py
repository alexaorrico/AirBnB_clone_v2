#!/usr/bin/python3
"""A script that starts a Flask web application"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/status')
def status():
    return jsonify({
        "status": "OK"
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

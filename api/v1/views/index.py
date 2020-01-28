#!/usr/bin/python3
"""status route"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)

@app_views.route('/status', strict_slashes=False)
def status():
    """ return a JSON """
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

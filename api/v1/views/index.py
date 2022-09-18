#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/status')
def status():
    """status view"""
    return jsonify({
                    "status": "OK"
                    })

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or '0.0.0.0',
    port=getenv("HBNB_API_PORT") or 5000,
    threaded=True)

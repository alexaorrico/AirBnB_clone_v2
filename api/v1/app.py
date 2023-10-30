#!/usr/bin/python3
"""
Flask app
"""

from flask import Flask, render_template, jsonify, url_for, make_response
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(e):
    """Close storage"""
    storage.close()

if __name__ == "__main__":
    """Flask runner"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port)
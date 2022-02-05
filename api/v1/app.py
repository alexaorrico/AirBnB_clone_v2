#!/usr/bin/python3
"""Mudule which contains the FLASK_APP and represents the entry point"""

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close(error):
    """Method wich tears down storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

#!/usr/bin/python3
"""
app
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))

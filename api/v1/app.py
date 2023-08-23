#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import Flask
from models import storage
app = Flask(__name__)

@app.teardown_appcontext
def app_teardown():
    """removes current SQLAlchemy session"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

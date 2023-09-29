#!/usr/bin/python3

"""Flask app"""

from flask import Flask, Blueprint, render_template, abort
from models import storage
from api.v1.views import app_views
import os

# assign host and post values
host = "0.0.0.0"
port = 5000

if "HBNB_API_HOST" in os.environ:
    host = os.environ.get("HBNB_API_HOST")
if "HBNB_API_PORT" in os.environ:
    port = int(os.environ.get("HBNB_API_PORT"))

# instance of Flask
app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def cleanup_app_context(arg):
    """Remove SQLAlchemy  Session"""
    storage.close()

if __name__ == '__main__':
    # run flask app
    app.run(host=host, port=port, threaded=True)
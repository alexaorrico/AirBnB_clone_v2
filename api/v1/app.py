#!/usr/bin/python3
"""Flask web service API"""

from flask import Flask
from models import storage
from api.v1.views import app_views  # Blueprint

app = Flask(__name__)

# Register app_views as blueprint
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(error=None):
    """ Called when application context is torn down"""
    storage.close()
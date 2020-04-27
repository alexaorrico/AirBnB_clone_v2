#!/usr/bin/python3
"""A script that starts a Flask web application"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(self):
    """Removes current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST') or '0.0.0.0',
            port=os.getenv('HBNB_API_PORT') or '5000',
            threaded=True)

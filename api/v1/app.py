#!/usr/bin/python3
"""main api program I think"""
import json
from flask import Flask, request, Blueprint
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def remove_session(exc):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

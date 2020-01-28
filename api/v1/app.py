#!/usr/bin/python3
"""Flask Module for a web application"""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """closes all storage sessions"""
    storage.close()

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=getenv('HBNB_API_PORT') or 5000, threaded=True)
